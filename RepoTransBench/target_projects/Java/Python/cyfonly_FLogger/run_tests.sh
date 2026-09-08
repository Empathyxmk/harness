#!/bin/bash
set -e
# Run all tests (original and public) using pytest
pytest tests/
pytest public_tests/