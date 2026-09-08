#!/bin/bash
set -e

echo "Running tests with coverage..."
coverage run --branch -m pytest tests
echo "Reporting coverage..."
coverage report -m