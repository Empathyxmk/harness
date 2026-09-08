#!/bin/bash
set -e

# Install dependencies if needed
pip install -r requirements.txt

# Run all tests in the project (original & public)
pytest tests/ public_tests/