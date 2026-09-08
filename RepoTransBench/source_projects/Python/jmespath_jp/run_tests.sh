#!/bin/bash
# Run Python tests with enforcement to avoid problem plugins and to maximize coverage.

echo "Running Python tests with coverage..."

export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

coverage run --branch -m pytest test_jp_wrapper.py