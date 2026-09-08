#!/bin/bash
set -e

# Activate virtualenv if present
if [ -d "./venv" ]; then
    source ./venv/bin/activate
fi

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

pip install pytest pytest-cov requests-mock

# Set a dummy API_KEY for unit tests to avoid KeyError
export API_KEY="dummy_key"

# Coverage run (unit + all discoverable/pytest style tests)
pytest --cov=cloudconvert --cov-branch --cov-report=term-missing --cov-report=html tests/unit