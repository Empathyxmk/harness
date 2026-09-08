#!/bin/bash
set -e

echo "Running all tests (original and public)..."
pytest tests
pytest public_tests