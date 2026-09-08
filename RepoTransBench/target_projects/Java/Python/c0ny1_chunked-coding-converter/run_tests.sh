#!/bin/bash
set -e

# Runs both original and public tests
echo "Running all tests (original + public)..."
pytest --tb=short -v tests/ public_tests/