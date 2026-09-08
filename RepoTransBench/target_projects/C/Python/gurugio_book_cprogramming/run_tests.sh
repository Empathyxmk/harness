#!/bin/bash
set -e
echo "Building and running all tests..."
pytest tests/original/ -v
echo "All tests passed!"