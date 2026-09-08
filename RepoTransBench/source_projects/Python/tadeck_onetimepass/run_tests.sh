#!/bin/bash
set -e

# Install dependencies for production and tests
pip install -r requirements/production.txt
pip install -r requirements/tests.txt || true

# Run coverage with unittest including all tests, then show the report
coverage run --branch --source=onetimepass -m unittest discover -s tests -p "*.py"
coverage report