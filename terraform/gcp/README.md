# Terraform for GCP Cloud Run Deployment

This Terraform configuration deploys the FastAPI backend to Google Cloud Run with an Artifact Registry Docker repository. It:
- Creates an Artifact Registry repository (Docker format)
- Creates a service account for Cloud Run runtime
- Grants necessary IAM roles (artifactregistry.reader, logging.logWriter)
- Deploys a Cloud Run (fully managed) service on port 8080
- Allows unauthenticated invocation (public access)
- Outputs the service URL

## Prerequisites

- gcloud CLI installed and authenticated
- Terraform >= 1.5.0
- A GCP project with billing enabled
- APIs enabled:
  - Artifact Registry API
  - Cloud Run Admin API
  - Cloud Build API (if using cloud build)
  - IAM API
- Docker installed to build the image

Enable required APIs (example):
```
gcloud services enable artifactregistry.googleapis.com run.googleapis.com iam.googleapis.com
```

## Variables

- project_id (required): Your GCP project ID
- region (default: us-central1)
- service_name (default: immortal-jellyfish-fact-api)
- repository_id (default: app-backend)
- image_tag (default: latest)
- cpu (default: 1)
- memory (default: 512Mi)
- min_instances (default: 0)
- max_instances (default: 10)
- env (default: {}): Optional environment variables map

## Build and Push the Image

From the repository root:
```
PROJECT_ID="<your-project-id>"
REGION="us-central1"
REPO_ID="app-backend"
SERVICE_NAME="immortal-jellyfish-fact-api"
IMAGE_TAG="latest"

# Create AR repository (Terraform can create it too; run apply once or create manually)
# Using Terraform init/apply is recommended to create it.

# Configure Docker authentication for Artifact Registry
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Build
cd immortal-jellyfish-fact-api-209930-209939/inference_api_backend
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_ID}/${SERVICE_NAME}:${IMAGE_TAG} .

# Push
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_ID}/${SERVICE_NAME}:${IMAGE_TAG}
```

## Deploy with Terraform

From the Terraform directory:
```
cd immortal-jellyfish-fact-api-209930-209939/terraform/gcp

terraform init

terraform apply \
  -var="project_id=${PROJECT_ID}" \
  -var="region=${REGION}" \
  -var="repository_id=${REPO_ID}" \
  -var="service_name=${SERVICE_NAME}" \
  -var="image_tag=${IMAGE_TAG}"
```

After apply completes, Terraform will output:
- service_url: the public URL to access your Cloud Run service.

## Notes

- The Dockerfile exposes port 8080 and runs uvicorn, which Cloud Run will access using PORT env var (defaults to 8080).
- The configuration allows unauthenticated access using Cloud Run IAM policy (roles/run.invoker to allUsers).
- Update variables in variables.tf or pass via -var to tailor deployment.
- Set env variables (like CORS allowances) by passing a map, e.g.:
```
-var='env={ APP_VERSION="1.0.0", CORS_ALLOW_ORIGINS="*" }'
```
