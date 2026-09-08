#!/bin/bash
set -e

# Install requirements (idempotent for local venv or CI)
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

# Run all tests with coverage report, using pytest
pytest --cov=src tests/ public_tests/