terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.44"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.44"
    }
  }
}

# Configure the Google Cloud provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# Some Cloud Run features can be gated in beta; keep available if needed
provider "google-beta" {
  project = var.project_id
  region  = var.region
}
