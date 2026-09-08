#!/bin/bash
set -e

# Simple test execution script for full test suite
# Runs both original and public tests

echo "Running all tests with pytest..."
pytest tests/ public_tests/