#!/bin/bash
set -e

# Run all tests in both original and public test dirs
pytest tests/original
pytest public_tests