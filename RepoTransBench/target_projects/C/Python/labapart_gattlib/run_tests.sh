#!/bin/bash
set -e

echo "Setting up Python environment..."
# Check if python3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python not found. Please install Python 3."
    exit 1
fi

# Ensure pytest is installed
if ! $PYTHON_CMD -c "import pytest" &> /dev/null; then
    echo "pytest not found. Installing dependencies from requirements.txt..."
    $PYTHON_CMD -m pip install -r requirements.txt
fi

echo "Running tests..."
# Add src/ to PYTHONPATH so the gattlib mock module can be found
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# Run all tests using pytest
# -v for verbose output
# --strict-markers to warn about unknown markers (good practice)
# --exit-first to stop on first failure (optional, can be removed)
$PYTHON_CMD -m pytest -v tests/original/ public_tests/
echo "All tests executed."