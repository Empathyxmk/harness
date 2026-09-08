#!/bin/bash
set -e
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest --maxfail=1 --disable-warnings public_tests/