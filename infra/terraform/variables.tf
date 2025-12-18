variable "project_id" {
  description = "The GCP project ID to deploy into."
  type        = string
}

variable "region" {
  description = "GCP region for Cloud Run (e.g., us-central1)."
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Cloud Run service name."
  type        = string
  default     = "immortal-jellyfish-inference"
}

variable "container_image" {
  description = "Full URI of the container image to deploy (e.g., us-docker.pkg.dev/PROJECT/REPO/image:TAG or gcr.io/PROJECT/image:TAG)."
  type        = string
  default     = "gcr.io/PROJECT/immortal-jellyfish-inference:TAG"
}
