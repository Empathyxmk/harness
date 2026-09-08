#!/bin/bash
set -e

# Install requirements if needed. Uncomment the next line if running outside of a managed environment.
# pip install -r requirements.txt

echo "Running all Python tests using pytest..."
pytest
echo "All Python tests ran."