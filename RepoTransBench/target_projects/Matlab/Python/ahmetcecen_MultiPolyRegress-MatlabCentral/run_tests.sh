#!/bin/bash
set -e

# Add src folder to PYTHONPATH for imports from tests
export PYTHONPATH="$PYTHONPATH:$(pwd)/src"
pytest tests
pytest public_tests