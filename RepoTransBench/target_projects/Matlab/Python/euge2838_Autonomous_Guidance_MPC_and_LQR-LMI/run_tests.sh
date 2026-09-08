#!/bin/bash
set -e
# Install requirements if not already installed
pip install -r requirements.txt > /dev/null

echo "Running all tests (original and public)..."
pytest

echo ""
echo "Running only original tests..."
pytest tests/original/

echo ""
echo "Running only public tests..."
pytest public_tests/