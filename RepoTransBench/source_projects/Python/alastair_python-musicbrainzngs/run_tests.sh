#!/bin/bash
set -e
coverage erase || true

# Use coverage directly to run pytest, avoiding the need for pytest-cov plugin
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
coverage run --branch -m pytest --maxfail=1 --disable-warnings test/

# Print text summary
coverage report --skip-covered --show-missing
coverage html