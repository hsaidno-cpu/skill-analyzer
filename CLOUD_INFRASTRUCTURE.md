# SKILL ANALYZER — Production infrastructure

The cloud runtime code is in service/. Production infrastructure is provisioned through Terraform in infra/gcp/README.md.

## Provisioned components

- Google Cloud Run Gen 2 runtime.
- Memorystore Redis Standard HA with private VPC/Private Service Access connectivity.
- Artifact Registry for application images.
- Secret Manager for runtime credentials.
- Global HTTPS load balancer, Google-managed TLS, and Cloud DNS.
- GitHub Actions deployment through Workload Identity Federation (no long-lived service-account JSON key).

The deployment guide covers project, billing, domain, DNS delegation, identity-provider, model-provider, secret, and initial deployment steps.

## Important

This repository contains infrastructure-as-code and a deployment workflow. It does not create a cloud account, purchase a domain, or fabricate real credentials. Applying the Terraform configuration requires an existing billed Google Cloud project, a domain the operator controls, a real OIDC issuer, and a real model-provider API key.

Never commit credentials or Terraform state. Use Secret Manager for runtime secrets, a private versioned GCS bucket for Terraform state, and GitHub OIDC/WIF for CI/CD.
