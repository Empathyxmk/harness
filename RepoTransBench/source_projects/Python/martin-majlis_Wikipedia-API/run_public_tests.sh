#!/bin/bash
# Run public tests with correct PYTHONPATH
PYTHONPATH="$(pwd)" PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest public_tests/