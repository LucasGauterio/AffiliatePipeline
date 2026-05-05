output "artifact_registry_repo" {
  value = google_artifact_registry_repository.pipeline_repo.name
}

output "service_account_email" {
  value = google_service_account.pipeline_sa.email
}

output "cloud_run_job_name" {
  value = google_cloud_run_v2_job.pipeline_job.name
}
