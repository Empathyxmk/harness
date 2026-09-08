#!/bin/bash
set -e

# Install test/development dependencies
pip install -r requirements_test.txt

# Run pytest on the tests directory
pytest tests