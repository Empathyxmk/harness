#!/bin/bash
pip install pytest coverage pytest-cov --quiet
echo "Running tests with coverage..."
coverage run --branch -m pytest