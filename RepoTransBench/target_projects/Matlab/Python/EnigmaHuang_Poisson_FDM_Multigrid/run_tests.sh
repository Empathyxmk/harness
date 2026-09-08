#!/bin/bash
set -e

echo "Running all Python tests with pytest..."
pytest --maxfail=5 --disable-warnings -v