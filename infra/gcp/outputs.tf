output "public_api_url" {
  description = "Public HTTPS base URL."
  value       = "https://${var.api_domain}"
}
output "mcp_endpoint" {
  description = "Remote MCP endpoint and exact OIDC audience."
  value       = "https://${var.api_domain}/mcp"
}
output "http_api_endpoint" {
  description = "HTTP JSON invocation endpoint."
  value       = "https://${var.api_domain}/v1/invoke"
}
output "load_balancer_ip" {
  description = "Global external IP reserved for the HTTPS load balancer."
  value       = google_compute_global_address.https.address
}
output "dns_name_servers" {
  description = "Delegate the root domain to these Cloud DNS nameservers at the registrar."
  value       = google_dns_managed_zone.public.name_servers
}
output "artifact_registry_repository" {
  description = "Docker image repository URL."
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.gateway.repository_id}"
}
output "runtime_service_account" {
  description = "Least-privilege Cloud Run runtime identity."
  value       = google_service_account.runtime.email
}
output "github_workload_identity_provider" {
  description = "Set as GCP_WORKLOAD_IDENTITY_PROVIDER GitHub Actions repository variable."
  value       = google_iam_workload_identity_pool_provider.github.name
}
output "github_deployer_service_account" {
  description = "Set as GCP_DEPLOY_SERVICE_ACCOUNT GitHub Actions repository variable."
  value       = google_service_account.github_deployer.email
}
output "terraform_state_bucket" {
  description = "Versioned private bucket for Terraform state."
  value       = google_storage_bucket.terraform_state.name
}
output "redis_private_host" {
  description = "Memorystore private IP. Keep it inside the VPC."
  value       = google_redis_instance.gateway.host
  sensitive   = true
}
output "secret_manager_secret_ids" {
  description = "Secret IDs. Add actual values only with gcloud Secret Manager commands."
  value = {
    llm_api_key     = google_secret_manager_secret.llm_api_key.secret_id
    audit_hash_salt = google_secret_manager_secret.audit_hash_salt.secret_id
    redis_url       = google_secret_manager_secret.redis_url.secret_id
  }
}
