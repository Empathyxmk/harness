#!/bin/bash
set -e

# Run all original and public tests
PYTHONPATH=src pytest tests/original/ public_tests/