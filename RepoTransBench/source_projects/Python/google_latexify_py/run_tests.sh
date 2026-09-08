#!/bin/bash
# Clean up .pyc, .pytest_cache, .coverage to ensure a fresh run.
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
rm -rf .pytest_cache .coverage htmlcov

# Explicitly tell pytest NOT to load external plugins.
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
coverage run --branch -m pytest src

coverage report --show-missing
coverage html