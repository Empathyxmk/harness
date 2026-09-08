#!/bin/bash
set -e

# Assume all dependencies are installed. Just run tests and coverage.
if [ -f .coverage ]; then
    rm .coverage
fi

# Try both pytest and Django runner
coverage run --branch --source=django_google_maps,sample manage.py test
coverage report -m
coverage html || true