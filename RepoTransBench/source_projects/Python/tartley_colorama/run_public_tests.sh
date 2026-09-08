#!/bin/bash
echo "Running public pytest suite..."
# Try several variants to ensure pytest is found
if command -v pytest &> /dev/null
then
    pytest public_tests/
elif command -v python3 &> /dev/null && python3 -m pytest --version &> /dev/null
then
    python3 -m pytest public_tests/
elif command -v python &> /dev/null && python -m pytest --version &> /dev/null
then
    python -m pytest public_tests/
else
    echo "pytest is not installed or not found in PATH, attempting install and run with python3 -m pytest..."
    pip install pytest
    python3 -m pytest public_tests/
fi