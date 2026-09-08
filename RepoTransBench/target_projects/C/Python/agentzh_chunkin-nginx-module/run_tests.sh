#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running all tests (original and public)..."
pytest tests/original/ public_tests/