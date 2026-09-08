#!/bin/bash
set -e
echo "Cleaning previous .coverage files..."
rm -f .coverage
echo "Running all tests with pytest & coverage..."

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 coverage run --branch -m pytest tests
coverage report --show-missing
coverage html