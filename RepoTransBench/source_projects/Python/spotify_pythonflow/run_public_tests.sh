#!/bin/bash
# Add project root (where pythonflow is) to PYTHONPATH to allow module imports for public tests

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

echo "Running public tests..."
pytest public_tests/