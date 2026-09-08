#!/bin/bash
set -e

# Install dependencies if not present
pip install -r requirements.txt

# Run all tests (original and public)
pytest tests/ public_tests/