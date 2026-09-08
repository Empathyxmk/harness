#!/bin/bash

set -e

# Run all original tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing

# Generate coverage report
coverage report -m > coverage.log
grep -E "TOTAL" coverage.log

echo "All tests completed successfully!"