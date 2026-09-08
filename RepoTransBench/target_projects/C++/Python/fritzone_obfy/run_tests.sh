#!/bin/bash
set -e

# Install dependencies (if not already)
pip install -r requirements.txt

# Run all tests (original and public)
pytest tests/original
pytest public_tests