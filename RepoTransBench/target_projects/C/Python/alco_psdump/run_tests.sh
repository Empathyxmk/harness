#!/bin/bash
set -e

# Add src/ to PYTHONPATH so Python can find the package
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

echo "Running all tests (original and public)..."
pytest

echo "All tests executed successfully."