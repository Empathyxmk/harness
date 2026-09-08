#!/bin/bash
set -e

# Install Python dependencies
pip install -r requirements.txt

# Run all tests using pytest
# pytest automatically discovers tests in `tests/` and `public_tests/`
pytest