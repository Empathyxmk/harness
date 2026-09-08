#!/bin/bash
export PYTHONWARNINGS=ignore
rm -f .coverage
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 coverage run --branch -m pytest public_tests
coverage report --show-missing