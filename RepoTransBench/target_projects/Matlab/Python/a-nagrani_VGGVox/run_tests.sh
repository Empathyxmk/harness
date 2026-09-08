#!/bin/bash
set -e
echo "Running all Python tests..."
pytest tests/original/
pytest public_tests/