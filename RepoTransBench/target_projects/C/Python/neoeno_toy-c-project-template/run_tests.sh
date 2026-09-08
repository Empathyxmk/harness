#!/bin/bash
set -e

echo "--- Installing Python dependencies ---"
pip install -r requirements.txt

echo "--- Running all tests with pytest ---"
# Using -v for verbose output, -s to show print statements (though none in tests),
# and --ignore to prevent pytest from discovering the original C files if they were present.
pytest -v