#!/bin/bash
set -e
# Run all Python tests using pytest in both tests/ and public_tests/ directories
pytest tests/
pytest public_tests/