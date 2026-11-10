locals {
  service_name = "skill-analyzer-gateway"
  mcp_url      = "https://\${var.api_domain}/mcp"
  public_url   = "https://\${var.api_domain}"
  secret_names = {
    llm_api_key     = "skill-analyzer-llm-api-key"
    audit_hash_salt = "skill-analyzer-audit-hash-salt"
    redis_url       = "skill-analyzer-redis-url"
  }
}

resource "google_project_service" "apis" {
  for_each = toset([
    "artifactregistry.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "dns.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "logging.googleapis.com",
    "redis.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "serviceusage.googleapis.com",
    "servicenetworking.googleapis.com",
    "sts.googleapis.com"
  ])
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_storage_bucket" "terraform_state" {
  name                        = "\${var.project_id}-skill-analyzer-tfstate"
  project                     = var.project_id
  location                    = var.state_bucket_location
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false
  versioning { enabled = true }
  labels = var.labels
  depends_on = [google_project_service.apis]
}

resource "google_artifact_registry_repository" "gateway" {
  project       = var.project_id
  location      = var.region
  repository_id = "skill-analyzer"
  description   = "Production container images for SKILL ANALYZER Gateway"
  format        = "DOCKER"
  labels        = var.labels
  depends_on    = [google_project_service.apis]
}

resource "google_compute_network" "gateway" {
  project                 = var.project_id
  name                    = "skill-analyzer-vpc"
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
  depends_on              = [google_project_service.apis]
}

resource "google_compute_subnetwork" "gateway" {
  project                  = var.project_id
  name                     = "skill-analyzer-\${var.region}"
  region                   = var.region
  network                  = google_compute_network.gateway.id
  ip_cidr_range            = "10.40.0.0/24"
  private_ip_google_access = true
}

resource "google_compute_global_address" "private_services" {
  project       = var.project_id
  name          = "skill-analyzer-private-services"
  address_type  = "INTERNAL"
  purpose       = "VPC_PEERING"
  network       = google_compute_network.gateway.id
  prefix_length = 16
}

resource "google_service_networking_connection" "private_services" {
  network                 = google_compute_network.gateway.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_services.name]
  depends_on              = [google_project_service.apis]
}

resource "google_redis_instance" "gateway" {
  project            = var.project_id
  name               = "skill-analyzer-redis"
  region             = var.region
  tier               = "STANDARD_HA"
  memory_size_gb     = var.redis_memory_gb
  redis_version      = "REDIS_6_X"
  connect_mode       = "PRIVATE_SERVICE_ACCESS"
  authorized_network = google_compute_network.gateway.id
  display_name       = "SKILL ANALYZER production rate-limit store"
  labels             = var.labels
  # No public Redis endpoint. Cloud Run accesses Redis over the private VPC path.
  depends_on = [google_service_networking_connection.private_services]
}

resource "google_secret_manager_secret" "llm_api_key" {
  project   = var.project_id
  secret_id = local.secret_names.llm_api_key
  replication { auto {} }
  labels     = var.labels
  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret" "audit_hash_salt" {
  project   = var.project_id
  secret_id = local.secret_names.audit_hash_salt
  replication { auto {} }
  labels     = var.labels
  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret" "redis_url" {
  project   = var.project_id
  secret_id = local.secret_names.redis_url
  replication { auto {} }
  labels     = var.labels
  depends_on = [google_project_service.apis]
}

# This is an internal RFC1918 endpoint, not a password or public credential.
resource "google_secret_manager_secret_version" "redis_url" {
  secret      = google_secret_manager_secret.redis_url.id
  secret_data = "redis://\${google_redis_instance.gateway.host}:\${google_redis_instance.gateway.port}/0"
}

resource "google_service_account" "runtime" {
  project      = var.project_id
  account_id   = "skill-analyzer-runtime"
  display_name = "SKILL ANALYZER Cloud Run runtime"
}

resource "google_secret_manager_secret_iam_member" "runtime_access" {
  for_each = {
    llm_api_key     = google_secret_manager_secret.llm_api_key.id
    audit_hash_salt = google_secret_manager_secret.audit_hash_salt.id
    redis_url       = google_secret_manager_secret.redis_url.id
  }
  project   = var.project_id
  secret_id = each.value
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:\${google_service_account.runtime.email}"
}

resource "google_iam_workload_identity_pool" "github" {
  project                   = var.project_id
  workload_identity_pool_id = "github-actions"
  display_name              = "GitHub Actions deployment"
  description               = "Keyless deployment identity for SKILL ANALYZER."
  depends_on                = [google_project_service.apis]
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "skill-analyzer-main"
  display_name                       = "SKILL ANALYZER main branch"
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }
  attribute_condition = "assertion.repository == '\${var.github_repository}' && assertion.ref == 'refs/heads/main'"
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account" "github_deployer" {
  project      = var.project_id
  account_id   = "skill-analyzer-github-deployer"
  display_name = "GitHub Actions deployer for SKILL ANALYZER"
}

resource "google_project_iam_member" "github_artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:\${google_service_account.github_deployer.email}"
}

resource "google_project_iam_member" "github_cloud_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:\${google_service_account.github_deployer.email}"
}

resource "google_service_account_iam_member" "github_runtime_user" {
  service_account_id = google_service_account.runtime.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:\${google_service_account.github_deployer.email}"
}

resource "google_service_account_iam_member" "github_wif_user" {
  service_account_id = google_service_account.github_deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/\${google_iam_workload_identity_pool.github.name}/attribute.repository/\${var.github_repository}"
}

resource "google_dns_managed_zone" "public" {
  project     = var.project_id
  name        = var.dns_zone_name
  dns_name    = var.dns_zone_dns_name
  description = "Public DNS zone for SKILL ANALYZER Gateway"
  visibility  = "public"
  depends_on  = [google_project_service.apis]
}

resource "google_compute_global_address" "https" {
  project      = var.project_id
  name         = "skill-analyzer-public-ip"
  address_type = "EXTERNAL"
  ip_version   = "IPV4"
}

resource "google_compute_managed_ssl_certificate" "gateway" {
  project = var.project_id
  name    = "skill-analyzer-managed-cert"
  managed {
    domains = [var.api_domain]
  }
  lifecycle { create_before_destroy = true }
}

resource "google_cloud_run_v2_service" "gateway" {
  count    = var.deploy_service ? 1 : 0
  project  = var.project_id
  name     = local.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"
  deletion_protection = true
  labels              = var.labels

  template {
    service_account                  = google_service_account.runtime.email
    timeout                          = "300s"
    max_instance_request_concurrency = 20
    scaling {
      min_instance_count = var.min_instance_count
      max_instance_count = var.max_instance_count
    }
    vpc_access {
      egress = "PRIVATE_RANGES_ONLY"
      network_interfaces {
        network    = google_compute_network.gateway.id
        subnetwork = google_compute_subnetwork.gateway.id
      }
    }
    containers {
      image = var.bootstrap_image
      ports { container_port = 8080 }
      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
      }
      env { name = "APP_ENV" value = "production" }
      env { name = "PUBLIC_BASE_URL" value = local.public_url }
      env { name = "MCP_RESOURCE_URL" value = local.mcp_url }
      env { name = "OIDC_ISSUER_URL" value = var.oidc_issuer_url }
      env { name = "OIDC_JWKS_URL" value = var.oidc_jwks_url }
      env { name = "OIDC_AUDIENCE" value = local.mcp_url }
      env { name = "OIDC_ALLOWED_ALGORITHMS" value = "RS256" }
      env { name = "LLM_BASE_URL" value = var.llm_base_url }
      env { name = "LLM_MODEL" value = var.llm_model }
      env { name = "RATE_LIMIT_BACKEND" value = "redis" }
      env { name = "RATE_LIMIT_PER_MINUTE" value = "20" }
      env { name = "MCP_ALLOWED_HOSTS" value = "\${var.api_domain},\${var.api_domain}:*" }
      env { name = "MCP_ALLOWED_ORIGINS" value = var.allowed_web_origins }
      env { name = "LOG_LEVEL" value = "INFO" }
      env {
        name = "LLM_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.llm_api_key.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "REDIS_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.redis_url.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "AUDIT_HASH_SALT"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.audit_hash_salt.secret_id
            version = "latest"
          }
        }
      }
    }
    depends_on = [
      google_secret_manager_secret_version.redis_url,
      google_secret_manager_secret_iam_member.runtime_access,
      google_service_networking_connection.private_services
    ]
  }
  depends_on = [google_project_service.apis]
  lifecycle {
    # Image tags are updated only by the GitHub Actions deployment workflow.
    ignore_changes = [template[0].containers[0].image]
  }
}

resource "google_cloud_run_v2_service_iam_member" "public_edge" {
  count    = var.deploy_service ? 1 : 0
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.gateway[0].name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_compute_region_network_endpoint_group" "gateway" {
  count                 = var.deploy_service ? 1 : 0
  project               = var.project_id
  name                  = "skill-analyzer-serverless-neg"
  region                = var.region
  network_endpoint_type = "SERVERLESS"
  cloud_run {
    service = google_cloud_run_v2_service.gateway[0].name
  }
}

resource "google_compute_backend_service" "gateway" {
  count                 = var.deploy_service ? 1 : 0
  project               = var.project_id
  name                  = "skill-analyzer-backend"
  protocol              = "HTTP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  timeout_sec           = 300
  backend {
    group = google_compute_region_network_endpoint_group.gateway[0].id
  }
}

resource "google_compute_url_map" "gateway" {
  count           = var.deploy_service ? 1 : 0
  project         = var.project_id
  name            = "skill-analyzer-https-map"
  default_service = google_compute_backend_service.gateway[0].id
}

resource "google_compute_target_https_proxy" "gateway" {
  count            = var.deploy_service ? 1 : 0
  project          = var.project_id
  name             = "skill-analyzer-https-proxy"
  url_map          = google_compute_url_map.gateway[0].id
  ssl_certificates = [google_compute_managed_ssl_certificate.gateway.id]
}

resource "google_compute_global_forwarding_rule" "https" {
  count                 = var.deploy_service ? 1 : 0
  project               = var.project_id
  name                  = "skill-analyzer-https-forwarding"
  target                = google_compute_target_https_proxy.gateway[0].id
  ip_address            = google_compute_global_address.https.address
  port_range            = "443"
  load_balancing_scheme = "EXTERNAL_MANAGED"
}

resource "google_compute_url_map" "http_redirect" {
  count   = var.deploy_service ? 1 : 0
  project = var.project_id
  name    = "skill-analyzer-http-redirect"
  default_url_redirect {
    https_redirect         = true
    strip_query            = false
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
  }
}

resource "google_compute_target_http_proxy" "http_redirect" {
  count   = var.deploy_service ? 1 : 0
  project = var.project_id
  name    = "skill-analyzer-http-proxy"
  url_map = google_compute_url_map.http_redirect[0].id
}

resource "google_compute_global_forwarding_rule" "http_redirect" {
  count                 = var.deploy_service ? 1 : 0
  project               = var.project_id
  name                  = "skill-analyzer-http-redirect-forwarding"
  target                = google_compute_target_http_proxy.http_redirect[0].id
  ip_address            = google_compute_global_address.https.address
  port_range            = "80"
  load_balancing_scheme = "EXTERNAL_MANAGED"
}

resource "google_dns_record_set" "gateway_a" {
  count        = var.deploy_service ? 1 : 0
  project      = var.project_id
  managed_zone = google_dns_managed_zone.public.name
  name         = "\${var.api_domain}."
  type         = "A"
  ttl          = 300
  rrdatas      = [google_compute_global_address.https.address]
}
