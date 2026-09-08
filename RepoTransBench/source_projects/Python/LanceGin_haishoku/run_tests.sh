#!/bin/bash
# Run all unit tests with coverage (line+branch), using pytest and pytest-cov if available, fallback to coverage+unittest otherwise

if command -v pytest > /dev/null 2>&1; then
  pytest --cov=haishoku --cov-report=term-missing --cov-branch tests/
  exit $?
else
  coverage run --branch -m unittest discover -s tests
  coverage report --omit='tests/*'
  exit $?
fi