#!/bin/bash
# Run public Python tests for jp_wrapper

echo "Running public Python tests..."

export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

pytest public_tests/test_public_jp_wrapper.py