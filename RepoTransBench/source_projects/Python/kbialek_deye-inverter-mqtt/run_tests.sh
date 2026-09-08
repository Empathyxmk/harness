#!/bin/bash
set -e

PYTHONPATH=src:plugins:$PYTHONPATH

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi
if [ -f requirements-dev.txt ]; then
  pip install -r requirements-dev.txt
fi

echo "Running tests with coverage..."

# Use unittest and coverage, include all subpackage sources
coverage run --branch --source=src,plugins -m unittest discover -s tests -p "*.py"
coverage report -m