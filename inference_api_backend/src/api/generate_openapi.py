import json
from pathlib import Path

from src.api.main import app


def main() -> None:
    """Generate OpenAPI JSON and write to interfaces/openapi.json."""
    openapi_schema = app.openapi()

    # Resolve to container root regardless of CWD
    base_dir = Path(__file__).resolve().parents[3]  # .../inference_api_backend
    output_dir = base_dir / "interfaces"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "openapi.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"Wrote OpenAPI schema to: {output_path}")


if __name__ == "__main__":
    main()
