variable "project_id" {
  description = "GCP project ID where resources will be created"
  type        = string
}

variable "region" {
  description = "GCP region for Artifact Registry and Cloud Run"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Cloud Run service name"
  type        = string
  default     = "immortal-jellyfish-fact-api"
}

variable "repository_id" {
  description = "Artifact Registry repository ID for container images"
  type        = string
  default     = "app-backend"
}

variable "image_tag" {
  description = "Container image tag to deploy from Artifact Registry"
  type        = string
  default     = "latest"
}

variable "cpu" {
  description = "vCPU allocated to Cloud Run container"
  type        = number
  default     = 1
}

variable "memory" {
  description = "Memory allocated to Cloud Run container"
  type        = string
  default     = "512Mi"
}

variable "max_instances" {
  description = "Maximum number of instances for the Cloud Run service"
  type        = number
  default     = 10
}

variable "min_instances" {
  description = "Minimum number of instances for the Cloud Run service"
  type        = number
  default     = 0
}

variable "env" {
  description = "Optional environment variables for the service (key-value map)"
  type        = map(string)
  default     = {}
}
