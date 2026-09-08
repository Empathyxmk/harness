#!/bin/bash
set -e

# Install dependencies if required
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# If tox, offer to run it
if [ -f tox.ini ]; then
    pip install tox
    tox
    exit 0
fi

# Use coverage for both tests.py and additional test files
if [ -f tests.py ]; then
    pip install --quiet coverage
    coverage run --branch -m unittest tests.py
fi

if [ -f test_check_manifest_additional.py ]; then
    coverage run --branch -m unittest test_check_manifest_additional.py || exit 1
fi

coverage combine
coverage report --show-missing