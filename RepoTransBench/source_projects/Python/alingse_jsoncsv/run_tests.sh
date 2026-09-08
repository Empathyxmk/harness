#!/bin/bash
set -e

echo "Running pytest with coverage for all tests..."
export PYTHONPATH=$(pwd)
# Disable external plugins: if using pytest >=7, use --no-plugin-auto-enable; fallback: use env var
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 coverage run --branch -m pytest tests
coverage report
coverage html