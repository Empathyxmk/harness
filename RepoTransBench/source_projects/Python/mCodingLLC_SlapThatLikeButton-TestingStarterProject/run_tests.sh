#!/bin/bash
set -e

# Optional: install dev dependencies
# pip install -r requirements.txt
# pip install -r requirements_dev.txt

# Ensure pytest and pytest-cov are installed
pip install pytest pytest-cov

# Run pytest with coverage, using src as package dir for slapping
PYTHONPATH=src pytest --cov=slapping tests