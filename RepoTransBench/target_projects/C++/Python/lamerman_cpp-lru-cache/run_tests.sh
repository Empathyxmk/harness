#!/bin/bash
set -e

# Run all Python tests using pytest (both tests/original and public_tests)
pytest tests/ public_tests/