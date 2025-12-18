# Terraform for GCP Cloud Run (Immortal Jellyfish Inference API)

This Terraform project deploys the FastAPI service to Google Cloud Run (fully managed).

Contents:
- versions.tf: Terraform and provider version pinning
- main.tf: Google provider, API enabling, Cloud Run service, and unauthenticated IAM
- variables.tf: Inputs (project_id, region, service_name, container_image)
- outputs.tf: Service name and public URL
- docker_image_placeholder.txt: Notes about the container image to supply

## Prerequisites

1) Google Cloud SDK (gcloud) installed and authenticated:
   gcloud auth login
   gcloud auth application-default login

2) A GCP project with billing enabled. Capture your project id:
   export TF_VAR_project_id="YOUR_GCP_PROJECT_ID"

3) Service enablement and permissions:
   - Terraform will enable required APIs (Cloud Run, Artifact Registry, Cloud Build).
   - Ensure your user or the service account used by Terraform has permissions to:
     - Enable services
     - Deploy Cloud Run services
     - Read the Artifact Registry or GCR image

4) Container image
   - Build and push your Docker image to GCR or Artifact Registry.
   - Provide the full image URI via var.container_image.
   - See docker_image_placeholder.txt for examples.

   Example (GCR):
   gcloud auth configure-docker
   docker build -t gcr.io/$TF_VAR_project_id/immortal-jellyfish-inference:v1 ./inference_api_backend
   docker push gcr.io/$TF_VAR_project_id/immortal-jellyfish-inference:v1

   Example (Artifact Registry):
   gcloud artifacts repositories create jellyfish --repository-format=docker --location=us-central1
   gcloud auth configure-docker us-central1-docker.pkg.dev
   docker build -t us-central1-docker.pkg.dev/$TF_VAR_project_id/jellyfish/immortal-jellyfish-inference:v1 ./inference_api_backend
   docker push us-central1-docker.pkg.dev/$TF_VAR_project_id/jellyfish/immortal-jellyfish-inference:v1

## Auth for Terraform

Terraform uses Application Default Credentials (ADC). Make sure you have:
- Run: gcloud auth application-default login
- Or set GOOGLE_APPLICATION_CREDENTIALS to a service account key file:
  export GOOGLE_APPLICATION_CREDENTIALS="/path/to/sa.json"

## Usage

From the infra/terraform directory:

1) Initialize:
   terraform init

2) Plan:
   terraform plan \
     -var "project_id=$TF_VAR_project_id" \
     -var "region=us-central1" \
     -var "service_name=immortal-jellyfish-inference" \
     -var "container_image=gcr.io/$TF_VAR_project_id/immortal-jellyfish-inference:v1"

3) Apply:
   terraform apply \
     -var "project_id=$TF_VAR_project_id" \
     -var "region=us-central1" \
     -var "service_name=immortal-jellyfish-inference" \
     -var "container_image=gcr.io/$TF_VAR_project_id/immortal-jellyfish-inference:v1" \
     -auto-approve

4) Outputs:
   - cloud_run_service_name
   - cloud_run_service_uri (public URL)

5) Test:
   curl -s $(terraform output -raw cloud_run_service_uri)/health

## Notes

- The service listens on port 3001 inside the container; Cloud Run maps HTTPS externally.
- The configuration allows unauthenticated access (public). Adjust IAM in main.tf if you need auth.
- Resource lifecycle ignores changes to the container image digest to avoid unnecessary diffs when tags update.
- Scale-to-zero is enabled with min_instance_count = 0. Tune scaling settings for your SLOs.

## Cleanup

terraform destroy \
  -var "project_id=$TF_VAR_project_id" \
  -var "region=us-central1" \
  -var "service_name=immortal-jellyfish-inference" \
  -var "container_image=gcr.io/$TF_VAR_project_id/immortal-jellyfish-inference:v1" \
  -auto-approve
