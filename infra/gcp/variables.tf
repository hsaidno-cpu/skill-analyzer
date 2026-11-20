variable "project_id" {
  description = "Existing Google Cloud project with billing enabled."
  type        = string
}
variable "region" {
  description = "Cloud Run and Memorystore region."
  type        = string
  default     = "asia-southeast1"
}
variable "api_domain" {
  description = "Public API hostname, for example api.example.com."
  type        = string
}
variable "dns_zone_name" {
  description = "Cloud DNS managed-zone resource name."
  type        = string
  default     = "skill-analyzer-public"
}
variable "dns_zone_dns_name" {
  description = "Root DNS zone with trailing dot, for example example.com."
  type        = string
}
variable "github_repository" {
  description = "GitHub owner/repository allowed to deploy through OIDC."
  type        = string
  default     = "hsaidno-cpu/skill-analyzer"
}
variable "bootstrap_image" {
  description = "Temporary container used until the first GitHub Actions deployment."
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}
variable "deploy_service" {
  description = "Create Cloud Run and public HTTPS load balancer after secrets and OIDC are ready."
  type        = bool
  default     = false
}
variable "oidc_issuer_url" {
  description = "Exact HTTPS issuer URI from the selected OIDC provider."
  type        = string
  default     = ""
}
variable "oidc_jwks_url" {
  description = "HTTPS JWKS endpoint from the selected OIDC provider."
  type        = string
  default     = ""
}
variable "llm_base_url" {
  description = "OpenAI-compatible Chat Completions API base URL."
  type        = string
  default     = "https://api.openai.com/v1"
}
variable "llm_model" {
  description = "Model identifier supported by the selected provider."
  type        = string
  default     = ""
}
variable "allowed_web_origins" {
  description = "Comma-separated browser origins allowed to reach the gateway. Empty for non-browser clients."
  type        = string
  default     = ""
}
variable "min_instance_count" {
  description = "Cloud Run minimum instances. Zero minimizes idle compute cost."
  type        = number
  default     = 0
}
variable "max_instance_count" {
  description = "Cloud Run maximum instances."
  type        = number
  default     = 10
}
variable "redis_memory_gb" {
  description = "Memorystore Redis Standard HA memory size in GiB."
  type        = number
  default     = 1
}
variable "state_bucket_location" {
  description = "Cloud Storage location for versioned Terraform state."
  type        = string
  default     = "ASIA-SOUTHEAST1"
}
variable "labels" {
  description = "Labels applied to supported resources."
  type        = map(string)
  default = {
    application = "skill-analyzer"
    managed_by  = "terraform"
    environment = "production"
  }
}
