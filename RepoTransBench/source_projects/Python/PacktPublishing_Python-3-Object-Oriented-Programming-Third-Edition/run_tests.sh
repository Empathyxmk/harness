#!/bin/bash
set -e

echo "Installing requirements"
pip install pytest coverage

echo "Running pytest with coverage..."
coverage run --branch -m pytest tests/
coverage report
coverage html

echo "All tests executed."