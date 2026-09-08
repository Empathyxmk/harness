#!/bin/bash
set -e
echo "Running public tests in public_tests/ with unittest..."
python3 -m unittest discover -s public_tests -p "test_public_*.py"