#!/bin/bash
set -e

# Run all original and public tests with pytest
pytest tests/original
pytest public_tests