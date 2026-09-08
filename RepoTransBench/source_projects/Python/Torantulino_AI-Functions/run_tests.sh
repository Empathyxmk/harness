#!/bin/bash
set -e

# Install dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Run tests with coverage, line + branch coverage, HTML + term report
pytest --cov=ai_functions --cov-report=term-missing --cov-report=html --cov-branch