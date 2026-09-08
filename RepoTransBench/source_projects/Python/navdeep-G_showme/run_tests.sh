#!/bin/bash
set -e

pip install -r requirements.txt

export PYTHONPATH="$PWD:$PYTHONPATH"

echo "Running all tests with coverage..."

coverage erase
coverage run --branch -m pytest showme/tests/
coverage report --show-missing