# Immortal Jellyfish Fact API

An inference API using FastAPI that returns a curated fact about the "immortal jellyfish" (Turritopsis dohrnii) and provides links to sources that both support and refute the claim.

## Repository layout
- inference_api_backend/
  - src/ -> FastAPI app code
  - interfaces/openapi.json -> generated OpenAPI schema
  - requirements.txt
  - Dockerfile

## Run locally
```
cd inference_api_backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001
```

Swagger UI: http://localhost:3001/docs  
OpenAPI JSON: http://localhost:3001/openapi.json

Generate OpenAPI file:
```
cd inference_api_backend
python -m src.api.generate_openapi
```

## Docker
```
cd inference_api_backend
docker build -t jellyfish-inference-api .
docker run -p 3001:3001 jellyfish-inference-api
```

## Endpoints
- GET / -> Root message with links to docs
- GET /health -> Health check
- GET /v1/fact -> Curated fact payload
- GET /v1/sources -> Only supporting/refuting sources

## Testing and Deployment
- The service is self-contained and uses only standard libs plus FastAPI stack.
- CI/CD and Terraform are out of scope for this specific step; add as needed.