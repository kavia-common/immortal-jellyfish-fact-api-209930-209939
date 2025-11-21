# Artifact Registry (Docker) repository for container images
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.repository_id
  description   = "Container images for ${var.service_name}"
  format        = "DOCKER"

  # Enable cleanup policies and other options later if needed
}

# Service account for Cloud Run runtime
resource "google_service_account" "run_sa" {
  account_id   = "${var.service_name}-sa"
  display_name = "Cloud Run runtime SA for ${var.service_name}"
}

# Allow the service account to read images from Artifact Registry
resource "google_project_iam_member" "artifact_registry_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.run_sa.email}"
}

# Allow the service account to write logs
resource "google_project_iam_member" "logging_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.run_sa.email}"
}

# Allow unauthenticated invocations (Public)
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

# Full image path we expect to deploy (push this image before apply or re-run apply after push)
locals {
  repo_hostname = "${var.region}-docker.pkg.dev"
  image_path    = "${local.repo_hostname}/${var.project_id}/${var.repository_id}/${var.service_name}:${var.image_tag}"
}

# Cloud Run service (fully managed)
resource "google_cloud_run_v2_service" "service" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL" # allow public

  template {
    service_account = google_service_account.run_sa.email

    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    containers {
      image = local.image_path

      # Cloud Run sets PORT; our Dockerfile defaults to 8080; keep containerPort 8080
      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = tostring(var.cpu)
          memory = var.memory
        }
      }

      # Optional environment variables
      dynamic "env" {
        for_each = var.env
        content {
          name  = env.key
          value = env.value
        }
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  # Ensure IAM binding for unauthenticated is applied after service exists
  depends_on = [
    google_project_iam_member.artifact_registry_reader,
    google_project_iam_member.logging_writer,
  ]
}

# Bind unauthenticated invoker to the service
resource "google_cloud_run_v2_service_iam_policy" "noauth" {
  location    = google_cloud_run_v2_service.service.location
  name        = google_cloud_run_v2_service.service.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
