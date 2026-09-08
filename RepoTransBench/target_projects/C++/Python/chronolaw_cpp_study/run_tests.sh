#!/bin/bash
set -e

echo "Running all Python tests with pytest"
pytest tests/original/
pytest public_tests/
pytest
echo "All available tests finished."