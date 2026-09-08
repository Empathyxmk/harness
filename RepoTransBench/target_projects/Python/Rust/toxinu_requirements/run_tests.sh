#!/bin/bash
export PYTHONWARNINGS=ignore
# Clean .coverage each time
rm -f .coverage
# disable 3rd-party pytest plugins that break things
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 coverage run --branch -m pytest tests
coverage report --show-missing