#!/bin/bash
set -e

# Run all tests in both original and public locations
pytest tests/original
pytest public_tests