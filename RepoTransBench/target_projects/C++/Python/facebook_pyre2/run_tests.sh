#!/bin/bash
set -e
echo "Running all tests with pytest and coverage..."
coverage run --source=re2 -m pytest
coverage report -m