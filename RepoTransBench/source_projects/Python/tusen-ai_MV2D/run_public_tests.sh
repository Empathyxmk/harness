#!/bin/bash
set -e

echo "Installing pytest for public tests..."
pip install pytest

echo "===== Running all public tests in ./public_tests/ ====="
pytest public_tests/