#!/bin/bash
set -e

# Remove existing .coverage data (just in case)
rm -f .coverage

# Install dependencies for public tests
pip install "pytest>=8.0.0,<9.0.0"

# Run only public tests
pytest public_tests/ --maxfail=1 --disable-warnings -v