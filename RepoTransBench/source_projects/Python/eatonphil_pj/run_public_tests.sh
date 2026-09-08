#!/bin/bash
set -e

# Install test dependencies if needed
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Run only public tests
python3 -m unittest discover -s public_tests -p "test_public_*.py"