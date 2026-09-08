#!/bin/bash
set -e

# Install the project in editable mode
pip install -e .

# Ensure pytest is available in case some tests want it
pip install pytest

# Set Django settings module for test environment
export DJANGO_SETTINGS_MODULE=tests.settings

# Run Django test suite via manage.py for DB setup/migrations handling
python manage.py test --verbosity=2