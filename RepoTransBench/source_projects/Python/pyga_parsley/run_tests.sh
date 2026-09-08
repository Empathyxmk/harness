#!/bin/bash
set -e

echo "Running all tests with coverage..."

# Remove any old .coverage file
rm -f .coverage

COVERAGE_PATHS="parsley.py setup.py ometa/builder.py ometa/vm_builder.py ometa/interp.py"
COVER_TESTS=$(find tests ometa/test terml/test examples -name 'test_*.py' | tr '\n' ' ')

# Run coverage on relevant sources and all test files
python3 -m coverage run --branch --source=parsley,ometa,terml --module pytest $COVER_TESTS

python3 -m coverage report --show-missing
python3 -m coverage html

echo "To view detailed coverage, see htmlcov/index.html"