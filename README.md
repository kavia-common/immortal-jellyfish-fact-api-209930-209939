# Immortal Jellyfish Fact API

An inference API using FastAPI that returns a curated fact about the "immortal jellyfish" (Turritopsis dohrnii) and provides links to sources that both support and refute the claim.

## Repository layout
- inference_api_backend/
  - src/ -> FastAPI app code
  - interfaces/openapi.json -> generated OpenAPI schema
  - requirements.txt
  - Dockerfile
  - Makefile
- infra/terraform -> Terraform for GCP Cloud Run
- interfaces/openapi.json -> optional top-level copy (for convenience/tools)

## Run locally (uvicorn)
```
cd inference_api_backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001
```
Open in browser:
- Swagger UI: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

## Run tests
```
cd inference_api_backend
make install
make test
# or with coverage
make cov
```

## Lint
```
cd inference_api_backend
make lint
```

## Generate OpenAPI (writes to inference_api_backend/interfaces/openapi.json)
```
cd inference_api_backend
python -m src.api.generate_openapi
```
Notes:
- The generator writes to inference_api_backend/interfaces/openapi.json regardless of your current working directory.
- If you need a top-level copy, copy it to ../interfaces/openapi.json.

## Docker
The Dockerfile runs uvicorn on 0.0.0.0:3001.
```
cd inference_api_backend
docker build -t jellyfish-inference-api .
docker run -p 3001:3001 jellyfish-inference-api
```

## CI summary
- Typical CI pipeline would run: lint, tests, coverage, and optionally generate OpenAPI and publish artifacts.
- This repo includes a Makefile with the above targets for easy CI integration:
  - make lint
  - make test
  - make cov
  - make openapi

## Terraform (GCP Cloud Run)
Terraform configuration is under infra/terraform. Review its README for full instructions.

Quick steps:
1) Build and push an image (example with GCR):
```
export PROJECT_ID="your-project-id"
gcloud auth configure-docker
docker build -t gcr.io/${PROJECT_ID}/immortal-jellyfish-inference:v1 ./inference_api_backend
docker push gcr.io/${PROJECT_ID}/immortal-jellyfish-inference:v1
```
2) Deploy with Terraform:
```
cd infra/terraform
terraform init
terraform apply \
  -var "project_id=${PROJECT_ID}" \
  -var "region=us-central1" \
  -var "service_name=immortal-jellyfish-inference" \
  -var "container_image=gcr.io/${PROJECT_ID}/immortal-jellyfish-inference:v1" \
  -auto-approve
```
3) Test:
```
curl -s $(terraform output -raw cloud_run_service_uri)/health
```

## Endpoints
- GET / -> Root message with links to docs
- GET /health -> Health check
- GET /v1/fact -> Curated fact payload
- GET /v1/sources -> Only supporting/refuting sources