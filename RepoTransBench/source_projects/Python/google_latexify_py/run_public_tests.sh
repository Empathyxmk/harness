#!/bin/bash
# Run all public test files in the public_tests directory
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest public_tests --maxfail=1 --disable-warnings -q