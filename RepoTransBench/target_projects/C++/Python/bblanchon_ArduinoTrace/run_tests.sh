#!/bin/bash
set -e

# Install dependencies if in a clean environment (optional for CI)
# pip install -r requirements.txt

pytest tests/original/
pytest public_tests/