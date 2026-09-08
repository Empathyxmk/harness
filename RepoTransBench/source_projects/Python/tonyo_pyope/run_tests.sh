#!/bin/bash
set -e
echo "Cleaning up old coverage data..."
rm -f .coverage
echo "Running tests with pytest and coverage (branch)..."
coverage run --branch -m pytest tests
coverage report
coverage html