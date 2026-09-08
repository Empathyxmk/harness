#!/bin/bash
set -e

# Run all tests, including original and public
pytest tests/
pytest public_tests/