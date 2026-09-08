#!/bin/bash
set -e

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

# Upgrade pip if necessary (skip if pip is broken)
pip --version || python3 -m ensurepip

# Install main requirements if exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || true
fi

# Also install test/demo requirements if exists
if [ -f "demo/requirements.txt" ]; then
    pip install -r demo/requirements.txt || true
fi

pip install pytest coverage pytest-cov tornado six

# Run test suite with coverage
coverage run --branch -m pytest plop/test
coverage report --skip-covered
coverage html