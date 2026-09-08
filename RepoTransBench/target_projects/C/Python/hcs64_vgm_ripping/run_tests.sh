#!/bin/bash
set -e

echo "Running all tests for hcs64_vgm_ripping..."

# Install the package in development mode if needed
pip install -e .

# Run all tests (both original and public)
python -m pytest tests/original public_tests -v

echo "All tests ran successfully."