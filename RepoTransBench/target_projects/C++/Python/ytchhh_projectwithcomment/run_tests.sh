#!/bin/bash
set -e

# Run all tests in both the public_tests and tests directories
pytest public_tests
pytest tests