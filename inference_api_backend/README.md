# Inference API Backend (FastAPI)

This container provides a FastAPI-based HTTP API that delivers a fact about the "immortal jellyfish" (Turritopsis dohrnii) and includes links to supporting and refuting sources. It includes typed models, a generated OpenAPI spec, unit tests, Docker assets, and Terraform for GCP Cloud Run deployment.

## Contents

- src/api/main.py: FastAPI application and health endpoints
- src/api/routers/facts.py: GET /v1/facts/immortal-jellyfish
- src/api/generate_openapi.py: Writes interfaces/openapi.json
- src/core/config.py: CORS configuration via environment variables
- src/core/version.py: Application version exposure
- src/domain/models.py: Pydantic models (Source, FactResponse, ErrorResponse)
- src/services/fact_service.py: Business logic returning curated fact and sources
- interfaces/openapi.json: Generated OpenAPI schema
- tests/test_health_and_facts.py: Unit tests for endpoints
- Dockerfile: Container build for Cloud Run

## API Overview

- Swagger UI: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json
- Generated spec file: interfaces/openapi.json

### Endpoints
- GET / → 200 {"status":"ok"}
- GET /health → 200 {"status":"ok"}
- GET /v1/facts/immortal-jellyfish → 200 FactResponse

Example:
```
GET http://localhost:3001/v1/facts/immortal-jellyfish

Response 200:
{
  "fact": "Turritopsis dohrnii can revert its mature medusa stage back to a juvenile polyp stage, allowing it to sidestep death under certain conditions. This phenomenon is sometimes described as 'biological immortality', but it does not prevent death from predation, disease, or unfavorable environments.",
  "supporting_sources": [
    {
      "title": "Reversing the life cycle: medusae reverting to polyps in Turritopsis",
      "url": "https://link.springer.com/article/10.1007/BF02391156",
      "note": "Peer-reviewed documentation of life cycle reversal (morphallaxis)."
    }
  ],
  "refuting_sources": [
    {
      "title": "No such thing as truly 'immortal' jellyfish",
      "url": "https://www.science.org/content/article/no-such-thing-immortal-jellyfish",
      "note": "Clarifies misuse of 'immortal' and real-world mortality factors."
    }
  ]
}
```

## Local Development

### Requirements
- Python 3.12
- pip

### Setup
```
cd immortal-jellyfish-fact-api-209930-209939/inference_api_backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### Run
```
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

### OpenAPI Generation
```
python -m src.api.generate_openapi
# Writes interfaces/openapi.json
```

## Testing

Run the tests:
```
pytest -q
```

## CI

A GitHub Actions workflow at .github/workflows/ci.yml installs dependencies and runs pytest. Extend it to add linting or build steps as needed.

## Docker

Build and run locally:
```
# From container root
cd immortal-jellyfish-fact-api-209930-209939/inference_api_backend

docker build -t immortal-jellyfish-fact-api:local .
docker run --rm -p 3001:8080 immortal-jellyfish-fact-api:local
```

- Service URL: http://localhost:3001
- Health: http://localhost:3001/health
- Docs: http://localhost:3001/docs

Pass environment variables:
```
docker run --rm -p 3001:8080 \
  -e APP_VERSION=1.0.0 \
  -e CORS_ALLOW_ORIGINS="*" \
  immortal-jellyfish-fact-api:local
```

## Terraform: Deploy to Google Cloud Run

Terraform files are under immortal-jellyfish-fact-api-209930-209939/terraform/gcp.

### Prerequisites
- Terraform >= 1.5.0
- gcloud authenticated; GCP project with billing
- Enable APIs:
  - artifactregistry.googleapis.com
  - run.googleapis.com
  - iam.googleapis.com
- Docker installed

Enable APIs example:
```
gcloud services enable artifactregistry.googleapis.com run.googleapis.com iam.googleapis.com
```

### Build and Push Image
```
PROJECT_ID="<your-project-id>"
REGION="us-central1"
REPO_ID="app-backend"
SERVICE_NAME="immortal-jellyfish-fact-api"
IMAGE_TAG="latest"

gcloud auth configure-docker ${REGION}-docker.pkg.dev

cd immortal-jellyfish-fact-api-209930-209939/inference_api_backend
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_ID}/${SERVICE_NAME}:${IMAGE_TAG} .
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_ID}/${SERVICE_NAME}:${IMAGE_TAG}
```

### Deploy with Terraform
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

To pass environment variables at deploy time:
```
terraform apply \
  -var="project_id=${PROJECT_ID}" -var="region=${REGION}" \
  -var="repository_id=${REPO_ID}" -var="service_name=${SERVICE_NAME}" \
  -var="image_tag=${IMAGE_TAG}" \
  -var='env={ APP_VERSION="1.0.0", CORS_ALLOW_ORIGINS="*" }'
```

After apply, note the output service_url to access your service.

## Configuration

Environment variables used by the app:
- APP_VERSION (optional; used in OpenAPI info.version)
- CORS_ALLOW_ORIGINS (comma-separated, default "*")
- CORS_ALLOW_METHODS (comma-separated, default "GET")
- CORS_ALLOW_HEADERS (comma-separated, default "*")
- CORS_ALLOW_CREDENTIALS ("true" or "false", default "true")
