# Immortal Jellyfish Fact API

A modular FastAPI backend that returns a curated fact about the "immortal jellyfish" (Turritopsis dohrnii) with supporting and refuting sources.

## Requirements
- Python 3.12
- pip

All dependencies are pinned in inference_api_backend/requirements.txt.

## Project Structure
- inference_api_backend/
  - src/
    - api/
      - main.py (FastAPI app)
      - generate_openapi.py (writes interfaces/openapi.json)
      - routers/
        - facts.py
    - core/
      - config.py
      - version.py
    - domain/
      - models.py
    - services/
      - fact_service.py
  - interfaces/
    - openapi.json (generated)

## Install
```
cd inference_api_backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Run the API
```
cd inference_api_backend
. .venv/bin/activate
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

Open:
- Swagger UI: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

## Endpoints
- GET / -> 200 { "status": "ok" }
- GET /health -> 200 { "status": "ok" }
- GET /v1/facts/immortal-jellyfish -> 200 FactResponse

## Generate OpenAPI
```
cd inference_api_backend
. .venv/bin/activate
python -m src.api.generate_openapi
# Writes interfaces/openapi.json
```

## Testing
Pytest is included. If tests are added:
```
cd inference_api_backend
. .venv/bin/activate
pytest -q
```

## Configuration
CORS can be configured via environment variables:
- CORS_ALLOW_ORIGINS
- CORS_ALLOW_METHODS
- CORS_ALLOW_HEADERS
- CORS_ALLOW_CREDENTIALS

Defaults allow GET from all origins.

## Deployment Notes
- Use uvicorn/gunicorn as ASGI server.
- The app object is available at src.api.main:app.
- Set APP_VERSION to expose a runtime version in OpenAPI metadata.
