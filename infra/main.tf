provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Artifact Registry for Docker Image
resource "google_artifact_registry_repository" "pipeline_repo" {
  provider      = google
  location      = var.region
  repository_id = "affiliate-pipeline-repo"
  description   = "Docker repository for Affiliate Pipeline"
  format        = "DOCKER"
}

# 2. Secret Manager
locals {
  secrets = ["WP_URL", "WP_USER", "WP_PASSWORD", "GEMINI_API_KEY"]
}

resource "google_secret_manager_secret" "secrets" {
  for_each  = toset(local.secrets)
  secret_id = each.key
  replication {
    auto {}
  }
}

# 3. Service Account for Cloud Run Job
resource "google_service_account" "pipeline_sa" {
  account_id   = "affiliate-pipeline-sa"
  display_name = "Service Account for Affiliate Pipeline Job"
}

resource "google_secret_manager_secret_iam_member" "secret_access" {
  for_each  = google_secret_manager_secret.secrets
  secret_id = each.value.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# 4. Cloud Run Job
resource "google_cloud_run_v2_job" "pipeline_job" {
  name     = "affiliate-pipeline-job"
  location = var.region

  template {
    template {
      service_account = google_service_account.pipeline_sa.email
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.pipeline_repo.name}/python-app:latest"
        
        env {
          name  = "ENV"
          value = "production"
        }
        env {
          name  = "GCP_PROJECT_ID"
          value = var.project_id
        }
      }
    }
  }
}

# 5. Cloud Scheduler
resource "google_cloud_scheduler_job" "pipeline_scheduler" {
  name             = "trigger-affiliate-pipeline"
  description      = "Triggers the Affiliate Pipeline Cloud Run Job"
  schedule         = var.schedule
  time_zone        = "America/Sao_Paulo"
  region           = var.region

  http_target {
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${google_cloud_run_v2_job.pipeline_job.name}:run"
    http_method = "POST"
    
    oauth_token {
      service_account_email = google_service_account.pipeline_sa.email
    }
  }
}

resource "google_project_iam_member" "scheduler_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}
