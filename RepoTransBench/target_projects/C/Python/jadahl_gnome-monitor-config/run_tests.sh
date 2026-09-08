#!/bin/bash
set -e
echo "Running all tests..."
python -m pytest tests/original/ public_tests/ -v