variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "schedule" {
  description = "Cron schedule for the Cloud Run Job"
  type        = string
  default     = "0 10 * * *" # Every day at 10 AM
}
