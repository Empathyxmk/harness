#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Running all tests..."
pytest

echo "All tests executed successfully."