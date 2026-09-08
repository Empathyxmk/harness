#!/bin/bash
set -e

echo "Running all Python tests..."
pytest --strict-markers -v

echo "All Python tests passed."