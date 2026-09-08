#!/bin/bash
set -e
# Run both original and public tests
pytest tests/original
pytest public_tests