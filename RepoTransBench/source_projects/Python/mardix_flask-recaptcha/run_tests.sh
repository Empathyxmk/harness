#!/bin/bash
# Remove .pytest_cache which may store bad plugins; run pytest without plugin discovery; exit on fail.
rm -rf .pytest_cache
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 coverage run --branch -m pytest