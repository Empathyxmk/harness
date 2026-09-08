#!/bin/bash
set -e

# Install dependencies if needed (optional for running in environments with pip, can comment out if not required)
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

# Add src/ to PYTHONPATH so msckf_mono is discoverable
export PYTHONPATH="$PYTHONPATH:$(pwd)/src"

# Run all tests in tests/original and public_tests
pytest tests/original/ public_tests/