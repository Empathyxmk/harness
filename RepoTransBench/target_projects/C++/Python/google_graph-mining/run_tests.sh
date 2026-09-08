#!/bin/bash
set -e
# Run all original and public tests with pytest (will find unittest and pytest style)
pytest tests/original/
pytest public_tests/