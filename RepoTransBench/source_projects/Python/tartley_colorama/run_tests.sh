#!/bin/bash
set -e

echo "Running pytest with coverage..."
coverage run --branch -m pytest colorama/tests
coverage report