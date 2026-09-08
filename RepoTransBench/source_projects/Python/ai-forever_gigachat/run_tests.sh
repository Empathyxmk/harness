#!/bin/bash
set -e

# Install dependencies via poetry and pip for dev
poetry install --with dev || poetry install

# Run pytest with coverage for both line and branch metrics, include all test directories
poetry run coverage run --branch -m pytest -v tests/unit_tests
poetry run coverage xml
poetry run coverage report