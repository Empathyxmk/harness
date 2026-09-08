#!/bin/bash
set -e

# Use virtualenv if present
if [ -d "venv" ]; then
  . venv/bin/activate
  export PYTHONPATH=.
fi

pip install --upgrade pip
if [ -f requirements_dev.txt ]; then pip install -r requirements_dev.txt; fi
pip install lxml

coverage run --branch -m unittest discover -s tests -v
coverage report
coverage html