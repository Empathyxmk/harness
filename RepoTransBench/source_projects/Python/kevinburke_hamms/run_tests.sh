#!/bin/bash
# Ensure flexmock isn't loaded to avoid pytest plugin issues
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
coverage run --branch -m pytest tests