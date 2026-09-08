#!/bin/bash
set -e

# Remove all __pycache__ directories to avoid import file mismatch issues
find . -type d -name '__pycache__' -exec rm -rf {} +

# Remove all .pyc files
find . -name '*.pyc' -delete

# Disable problematic plugins that may cause errors (like flexmock)
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

# Run pytest with coverage for ALL code_examples (all source + test dirs)
coverage run --branch --source=code_examples -m pytest code_examples/

coverage report
coverage html