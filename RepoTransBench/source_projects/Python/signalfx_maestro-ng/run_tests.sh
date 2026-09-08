#!/bin/bash
set -e

echo "=== Running flake8 for style checks ==="
flake8 maestro tests

echo "=== Running pytest with coverage ==="
coverage run --branch -m pytest -v
coverage report -m
coverage html