#!/bin/bash
set -e

# Ensure correct PATH for coverage when installed as a script
export PATH="${PATH}:$(python3 -m site --user-base)/bin"
export PYTHONPATH=.

echo "Running pytest with coverage for s3-pit-restore and setup.py..."

python3 -m coverage run --branch -m pytest tests
python3 -m coverage report -m