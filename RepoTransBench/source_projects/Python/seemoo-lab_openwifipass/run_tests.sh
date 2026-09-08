#!/bin/bash
# Run all tests using pytest+coverage and display output and HTML report

echo "Running tests with pytest and coverage..."
coverage run --branch -m pytest tests
coverage report --show-missing
coverage html