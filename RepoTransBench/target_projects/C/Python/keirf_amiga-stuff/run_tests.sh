#!/bin/bash
set -e

# Install dependencies if requirements.txt is newer than .venv/.deps
if [ -f requirements.txt ]; then
    if ! pip show pytest > /dev/null 2>&1; then
        echo "Installing Python test dependencies..."
        pip install -r requirements.txt
    fi
fi

# Run all original and public tests
echo "Running all tests with pytest..."
pytest

# Show exit code
exit $?