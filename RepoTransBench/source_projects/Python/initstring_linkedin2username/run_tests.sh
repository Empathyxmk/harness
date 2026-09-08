#!/bin/bash
# Clean up any previous pytest/flexmock cache that may interfere
rm -rf .pytest_cache .coverage htmlcov

# Unset any pytest plugins via environment
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

# Run pytest with coverage, disabling plugin autoload to avoid flexmock collection
coverage run --branch -m pytest --maxfail=3 --disable-warnings -v tests
coverage report
coverage html