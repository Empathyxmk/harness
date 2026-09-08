#!/bin/bash
set -e

# Simple script to run all tests with pytest
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt

echo "[INFO] Running all tests (original and public)..."
pytest tests/original/ public_tests/