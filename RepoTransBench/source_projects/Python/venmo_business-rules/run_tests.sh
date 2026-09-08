#!/bin/bash
set -e

# Install dependencies if requirements file exists
if [ -f "dev-requirements.txt" ]; then
    pip install -r dev-requirements.txt
fi

# Also install the package in editable mode if setup.py is present
if [ -f "setup.py" ]; then
    pip install -e .
fi

# Run pytest for the tests directory
pytest tests