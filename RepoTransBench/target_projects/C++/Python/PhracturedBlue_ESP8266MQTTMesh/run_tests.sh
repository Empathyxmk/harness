#!/bin/bash
set -e
python3 -m pip install --upgrade pip > /dev/null
python3 -m pip install -r requirements.txt > /dev/null

# Run all tests: both original and public
pytest tests/ public_tests/