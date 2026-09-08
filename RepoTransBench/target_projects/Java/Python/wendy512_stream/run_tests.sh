#!/bin/bash
set -e
# Run all tests (original and public)
pytest tests/
pytest public_tests/