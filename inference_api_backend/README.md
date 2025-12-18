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

## Quick start with curl

- Health check
```
curl -s http://localhost:3001/health | jq .
```

- Get curated fact (FactResponse)
```
curl -s http://localhost:3001/v1/fact | jq .
```

Example response (abbreviated):
```
{
  "fact": "Turritopsis dohrnii, often called the 'immortal jellyfish', can revert its adult medusa form back into a juvenile polyp...",
  "claim": "The species can avoid death from aging by reverting to an earlier life stage; however, it remains susceptible...",
  "supports": [
    { "url": "https://www.nature.com/articles/news.2010.490", "title": "Secrets of the 'immortal' jellyfish", "stance": "support" }
  ],
  "refutes": [
    { "url": "https://www.smithsonianmag.com/science-nature/there-no-such-thing-immortal-jellyfish-180974035/", "title": "There’s No Such Thing as an Immortal Jellyfish", "stance": "refute" }
  ],
  "retrieved_at": "2025-01-01T00:00:00Z",
  "version": "0.1.0"
}
```

- Get only sources
```
curl -s http://localhost:3001/v1/sources | jq .
```

Example response:
```
{
  "supports": [
    { "url": "https://www.nature.com/articles/news.2010.490", "title": "Secrets of the 'immortal' jellyfish", "stance": "support" }
  ],
  "refutes": [
    { "url": "https://www.smithsonianmag.com/science-nature/there-no-such-thing-immortal-jellyfish-180974035/", "title": "There’s No Such Thing as an Immortal Jellyfish", "stance": "refute" }
  ]
}
```

## Generate OpenAPI JSON to interfaces/openapi.json
```
cd inference_api_backend
python -m src.api.generate_openapi
```

This writes a fresh OpenAPI document to inference_api_backend/interfaces/openapi.json. Commit that file and optionally copy it to a top-level interfaces/ directory if your tooling expects it there.

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
