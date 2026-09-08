#!/bin/bash
set -e

# Install coverage tools if not present and run with coverage
if ! python3 -c "import coverage" 2>/dev/null; then pip3 install coverage; fi

python3 -m coverage run --branch -m unittest discover -s public_tests -p "test_public_*.py"
python3 -m coverage report