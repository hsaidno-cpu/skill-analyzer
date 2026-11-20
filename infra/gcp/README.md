# Production infrastructure — Google Cloud

This directory provisions the production foundation for the SKILL ANALYZER Cloud Gateway.

## Validation boundary

The repository CI runs Terraform formatting, provider initialization, and schema validation without cloud credentials. It does not run a production plan or apply. A real plan/apply requires the operator's authenticated Google Cloud project and chosen domain/OIDC/provider values.

## Selected topology

- Cloud Run Gen 2 in asia-southeast1 for the FastAPI + Remote MCP runtime.
- Memorystore for Redis, Standard HA tier, private service access only.
- Dedicated VPC and subnet; Cloud Run uses Direct VPC egress for Redis.
- Artifact Registry for immutable container images.
- Secret Manager for the model-provider API key, Redis URL, and audit HMAC salt.
- Global external Application Load Balancer, Google-managed TLS certificate, and Cloud DNS.
- GitHub Actions to Google Cloud Workload Identity Federation (WIF). No service-account JSON key is created.
- Application-level OAuth/OIDC bearer-token verification remains enabled. The public load-balancer edge is not a substitute for gateway authentication.

The project, billing account, domain registration, OIDC tenant, and provider account remain customer-owned prerequisites. Terraform creates resources inside an existing Google Cloud project; it does not create a billing account or purchase a domain.

## 1. Prerequisites

Install and authenticate:
- Terraform 1.6 or newer.
- Google Cloud CLI.
- A Google Cloud project with billing enabled and permissions to enable APIs, create IAM identities, VPC resources, Memorystore, Cloud Run, load balancing, DNS, Artifact Registry, and Secret Manager.
- A domain you own. The API hostname must be under the root DNS zone.
- An OIDC provider configured to issue signed JWT access tokens for the gateway audience and scope analyzer:invoke.
- An API key and model identifier for an OpenAI-compatible Chat Completions provider.

Example:
- API hostname: api.example.com
- Root DNS zone: example.com.

Do not use a domain you do not control.

## 2. Configure variables

~~~~bash
cp terraform.tfvars.example terraform.tfvars
~~~~

Edit terraform.tfvars:
- set the real project ID;
- set the domain and root DNS zone;
- set the issuer and JWKS URLs from your identity provider;
- set the model ID;
- leave deploy_service = false for the first apply.

The OIDC audience is not a free-form value. The deployment sets it to exactly https://<api-domain>/mcp, matching the service's runtime validation rule.

## 3. Authenticate and provision the foundation

~~~~bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login

terraform init -backend=false
terraform fmt -check
terraform validate
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
~~~~

The first apply creates the VPC, private Redis, Artifact Registry, empty Secret Manager secret containers, Cloud DNS zone, service accounts, GitHub WIF pool/provider, and a versioned private bucket for Terraform state. It does not yet create Cloud Run or the public load balancer.

### Move state into the private GCS backend

After the first apply succeeds, migrate local state to the versioned bucket:

~~~~bash
STATE_BUCKET="$(terraform output -raw terraform_state_bucket)"
terraform init -migrate-state \
  -backend-config="bucket=$STATE_BUCKET" \
  -backend-config="prefix=skill-analyzer/production"
~~~~

Keep the state bucket private. Terraform state contains resource metadata and may contain sensitive values in some providers. Do not upload state to GitHub or commit it.

## 4. Add production secret versions

The API key and audit salt secret containers are created by Terraform, but their secret values are deliberately not committed or supplied through Terraform variables.

Add the model-provider API key without placing its literal value in shell history:

~~~~bash
read -rsp "Model provider API key: " LLM_API_KEY
echo
printf %s "$LLM_API_KEY" | gcloud secrets versions add skill-analyzer-llm-api-key \
  --data-file=- --project=YOUR_PROJECT_ID
unset LLM_API_KEY
~~~~

Generate and store an independent audit pseudonymization salt:

~~~~bash
AUDIT_HASH_SALT="$(openssl rand -hex 32)"
printf %s "$AUDIT_HASH_SALT" | gcloud secrets versions add skill-analyzer-audit-hash-salt \
  --data-file=- --project=YOUR_PROJECT_ID
unset AUDIT_HASH_SALT
~~~~

Terraform creates a Redis URL secret version from the Memorystore private endpoint. Redis has no public endpoint; Cloud Run reaches it through the private VPC path.

The API key must belong to the provider selected in llm_base_url. Do not put it in terraform.tfvars, GitHub repository variables, source files, or commit messages.

## 5. Create the OIDC issuer and client

The gateway is an OAuth/OIDC resource server, not an identity provider. It validates tokens, but does not mint tokens or manage user logins.

A reference Auth0 setup is documented in ../identity/AUTH0.md. The issuer and JWKS URLs must match the exact values in terraform.tfvars. The API/resource audience must be exactly:

~~~~text
https://YOUR_API_DOMAIN/mcp
~~~~

The token must carry:
- a valid RS256 signature;
- the exact issuer;
- the exact audience above;
- a subject (sub);
- a valid expiry;
- scope analyzer:invoke.

After configuring the issuer, update variables and run terraform plan.

## 6. Create Cloud Run, TLS, DNS, and the load balancer

Before enabling the service, verify that the latest secret versions exist for:
- skill-analyzer-llm-api-key
- skill-analyzer-audit-hash-salt
- skill-analyzer-redis-url

Then change deploy_service to true and apply:

~~~~bash
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
~~~~

Terraform creates Cloud Run with private VPC egress, a serverless NEG, a global external HTTPS load balancer, a Google-managed certificate, an HTTP-to-HTTPS redirect, and the Cloud DNS A record pointing to the reserved global IP.

### Delegate DNS

Retrieve the authoritative Cloud DNS nameservers:

~~~~bash
terraform output dns_name_servers
~~~~

At your domain registrar, delegate the root domain to the returned Google Cloud DNS nameservers. Before moving an existing domain's nameservers, recreate unrelated MX, TXT, SPF, DKIM, verification, and other required DNS records in Cloud DNS. Otherwise, you can break mail or domain verification while trying to deploy an API.

The certificate becomes active only after public DNS points to the load balancer and Google can validate the hostname. Certificate provisioning is asynchronous. Check certificate status before treating HTTPS as live.

## 7. Configure GitHub Actions keyless deployment

Terraform outputs the identity values needed by the deployment workflow:

~~~~bash
terraform output -raw github_workload_identity_provider
terraform output -raw github_deployer_service_account
~~~~

In GitHub repository Settings → Secrets and variables → Actions → Variables, create these variables (not secrets):
- GCP_PROJECT_ID = your project ID;
- GCP_REGION = the configured region;
- GCP_WORKLOAD_IDENTITY_PROVIDER = the full provider resource name from Terraform output;
- GCP_DEPLOY_SERVICE_ACCOUNT = the deployer service-account email from Terraform output.

The WIF provider condition restricts tokens to hsaidno-cpu/skill-analyzer on refs/heads/main. The workflow receives short-lived federated credentials and does not use a downloaded service-account key. Deployments are triggered by relevant pushes to main or manually using workflow_dispatch.

The workflow builds an immutable image tag from the Git commit SHA, pushes it to Artifact Registry, and updates the existing Cloud Run service. Terraform intentionally ignores the container image field after bootstrap; the deployment workflow owns application image revisions.

## 8. Smoke checks

After DNS and certificate provisioning:

~~~~bash
curl -i https://YOUR_API_DOMAIN/healthz
curl -i https://YOUR_API_DOMAIN/readyz
curl -i https://YOUR_API_DOMAIN/.well-known/oauth-protected-resource/mcp
~~~~

A request without a bearer token to /v1/invoke must return 401. A valid token must include analyzer:invoke and the exact audience.

The health and readiness endpoints do not prove that the model provider can complete a billable inference call. Run a controlled test invocation and inspect Cloud Run logs for metadata-only audit events.

## 9. Cost and safety notes

This architecture creates billable resources. Memorystore Standard HA and the global external Application Load Balancer incur ongoing charges even when Cloud Run scales to zero. Start with the configured 1 GiB Redis tier and zero minimum Cloud Run instances, then review current regional prices before increasing capacity.

The Cloud Run service is invokable at the load-balancer edge because the application itself enforces OAuth/JWT authentication. If an organization policy blocks allUsers invoker, adjust the public load-balancer design deliberately; do not disable application-level authentication as a workaround.

Never commit terraform.tfvars, Terraform state or plan files, API keys, client secrets, Redis passwords, signing keys, or personal access tokens. Use Secret Manager for runtime secrets, the private versioned GCS backend for Terraform state, and WIF for CI/CD.
