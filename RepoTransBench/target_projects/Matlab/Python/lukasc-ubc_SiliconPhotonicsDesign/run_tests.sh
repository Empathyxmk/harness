#!/bin/bash
set -e

echo "Installing dependencies (if not already installed)..."
pip install -r requirements.txt

echo "Running all Python tests using pytest ..."
pytest tests/ public_tests/