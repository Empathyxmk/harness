#!/bin/bash
set -e
# Run all tests (original and public)
pytest tests/original
pytest public_tests