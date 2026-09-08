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

export API_KEY="dummy_public_key"

pytest public_tests/