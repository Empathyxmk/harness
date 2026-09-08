#!/bin/bash
set -e

# Install dependencies if not already installed
pip install -r requirements.txt

# Run all unit tests (original + public)
pytest tests/
pytest public_tests/