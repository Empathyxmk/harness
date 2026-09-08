#!/bin/bash
set -e

# Install dependencies, if needed
pip install -r requirements.txt

echo "Running ALL test cases with pytest..."
pytest