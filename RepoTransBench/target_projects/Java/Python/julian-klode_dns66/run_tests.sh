#!/bin/bash
set -e
# Runs all tests, both original and public, using pytest
pytest tests/original/
pytest public_tests/