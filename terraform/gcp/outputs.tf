output "service_url" {
  description = "Public URL for the Cloud Run service"
  value       = google_cloud_run_v2_service.service.uri
}
