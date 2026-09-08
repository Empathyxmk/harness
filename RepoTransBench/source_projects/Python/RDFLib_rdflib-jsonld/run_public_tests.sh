#!/bin/bash
# Run all *public* tests using pytest, ignore external plugins
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest public_tests/