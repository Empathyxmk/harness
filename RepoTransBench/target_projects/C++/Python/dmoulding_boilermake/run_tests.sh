#!/bin/bash
set -e

# Run all tests (both private/original and public)
pytest tests/
pytest public_tests/