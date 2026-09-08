#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Running all Python tests with pytest..."
pytest --import-mode=append

echo "All tests completed."