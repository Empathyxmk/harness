#!/bin/bash
# Minimal version to avoid pylama plugin interference
pip install -r requirements.txt pytest coverage pytest-cov > /dev/null

# Ensure pylama is not auto-loaded by pytest (can cause plugin errors if present)
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

coverage erase

# Run pytest with coverage, enabling branch coverage, terminal and html reports
coverage run --branch -m pytest
coverage report -m
coverage html