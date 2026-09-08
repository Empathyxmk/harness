#!/bin/bash
set -e

# Runs all tests using pytest across original and public test sets
pytest tests/
pytest public_tests/