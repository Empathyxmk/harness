#!/bin/bash
pip install pytest coverage pytest-cov jellyfish
echo "Running public tests with pytest..."
PYTHONPATH=. pytest us/public_tests/