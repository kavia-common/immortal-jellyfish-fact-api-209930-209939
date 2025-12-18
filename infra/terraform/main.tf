# Google provider configuration
provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required GCP APIs for Cloud Run deployment
resource "google_project_service" "run" {
  project                    = var.project_id
  service                    = "run.googleapis.com"
  disable_dependent_services = true
  disable_on_destroy         = false
}

resource "google_project_service" "artifact_registry" {
  project                    = var.project_id
  service                    = "artifactregistry.googleapis.com"
  disable_dependent_services = true
  disable_on_destroy         = false
}

resource "google_project_service" "cloudbuild" {
  project                    = var.project_id
  service                    = "cloudbuild.googleapis.com"
  disable_dependent_services = true
  disable_on_destroy         = false
}

# Create a Cloud Run (fully managed) service
resource "google_cloud_run_v2_service" "api" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL" # allow public ingress

  template {
    # Set minimum 0 instances to scale to zero
    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }

    # Container specification
    containers {
      image = var.container_image

      # Port exposed by the container; our FastAPI listens on 3001
      ports {
        container_port = 3001
      }

      # Basic CPU/memory recommendations for small API
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      # Environment variables (extend as needed)
      env {
        name  = "APP_NAME"
        value = "Immortal Jellyfish Inference API"
      }
      env {
        name  = "APP_VERSION"
        value = "0.1.0"
      }
    }
  }

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image # allow image tag digests to drift
    ]
  }

  depends_on = [
    google_project_service.run,
    google_project_service.artifact_registry,
    google_project_service.cloudbuild
  ]
}

# Allow unauthenticated invocations (public)
resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  project  = google_cloud_run_v2_service.api.project
  location = google_cloud_run_v2_service.api.location
  name     = google_cloud_run_v2_service.api.name

  role   = "roles/run.invoker"
  member = "allUsers"
}
