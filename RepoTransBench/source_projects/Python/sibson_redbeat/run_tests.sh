#!/bin/bash
set -e

# Run all tests with coverage, including branch coverage.
coverage run --branch -m pytest tests
coverage report --show-missing