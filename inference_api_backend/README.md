# Immortal Jellyfish Inference API (Backend)

A FastAPI service that returns a curated fact about the "immortal jellyfish" (Turritopsis dohrnii) and provides links to supporting and refuting sources.

## Features
- Endpoints:
  - GET / -> root message
  - GET /health -> health check
  - GET /v1/fact -> fact with sources (FactResponse)
  - GET /v1/sources -> only supporting and refuting sources
- OpenAPI/Swagger at /docs and schema at /openapi.json
- CORS configured (allow all by default) via environment variables

## Run locally

Using uvicorn:
```
cd inference_api_backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001
```

Using Docker:
```
cd inference_api_backend
docker build -t jellyfish-inference-api .
docker run -p 3001:3001 jellyfish-inference-api
```

Open in browser:
- Swagger UI: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

## Generate OpenAPI JSON to interfaces/openapi.json
```
cd inference_api_backend
python -m src.api.generate_openapi
```

## Configuration (Environment Variables)
- APP_NAME (default: Immortal Jellyfish Inference API)
- APP_DESCRIPTION
- APP_VERSION (default: 0.1.0)
- CORS_ALLOW_ORIGINS (comma-separated, default: *)
- CORS_ALLOW_CREDENTIALS (true/false, default: true)
- CORS_ALLOW_METHODS (default: *)
- CORS_ALLOW_HEADERS (default: *)

## Response Types

- FactResponse
  - fact: str
  - claim: str
  - supports: SourceLink[]
  - refutes: SourceLink[]
  - retrieved_at: datetime (UTC)
  - version: str

- SourceLink
  - url: HttpUrl
  - title: str
  - stance: "support" | "refute" | null
