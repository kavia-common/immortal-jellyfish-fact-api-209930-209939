output "cloud_run_service_name" {
  description = "Name of the deployed Cloud Run service."
  value       = google_cloud_run_v2_service.api.name
}

output "cloud_run_service_uri" {
  description = "Public URL of the deployed Cloud Run service."
  value       = google_cloud_run_v2_service.api.uri
}
