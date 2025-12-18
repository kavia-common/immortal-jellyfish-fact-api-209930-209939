.PHONY: help install lint test cov openapi

help:
\t@echo "Targets:"
\t@echo "  install  - install Python dependencies"
\t@echo "  lint     - run flake8 on src/ and tests/"
\t@echo "  test     - run pytest"
\t@echo "  cov      - run pytest with coverage"
\t@echo "  openapi  - generate interfaces/openapi.json"

install:
\tpython -m pip install --upgrade pip
\tpip install -r requirements.txt
\tpip install pytest-cov

lint:
\tflake8 src tests

test:
\tpytest -q --maxfail=1 --disable-warnings

cov:
\tpytest -q --maxfail=1 --disable-warnings --cov=src --cov-report=term --cov-report=xml

openapi:
\tpython -m src.api.generate_openapi
