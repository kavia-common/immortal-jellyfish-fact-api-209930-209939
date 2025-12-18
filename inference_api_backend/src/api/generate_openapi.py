import json
from pathlib import Path

from src.api.main import app


def main() -> None:
    """Generate OpenAPI JSON and write to interfaces/openapi.json under inference_api_backend.

    This script is safe to run from any working directory:
    - python -m src.api.generate_openapi
    The output will always be placed into the interfaces/ directory located directly
    under the inference_api_backend package root.
    """
    openapi_schema = app.openapi()

    # Resolve to inference_api_backend root regardless of CWD:
    # file path: <repo>/immortal-jellyfish-fact-api-.../inference_api_backend/src/api/generate_openapi.py
    # parents:
    # 0 generate_openapi.py
    # 1 api
    # 2 src
    # 3 inference_api_backend  <-- desired
    base_dir = Path(__file__).resolve().parents[3]
    output_dir = base_dir / "interfaces"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "openapi.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"Wrote OpenAPI schema to: {output_path}")


if __name__ == "__main__":
    main()
