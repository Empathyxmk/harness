#!/bin/bash
# Run tests with python -m unittest to avoid pytest plugins and use coverage
set -e
coverage run --branch -m unittest discover -s tests
coverage report --skip-covered