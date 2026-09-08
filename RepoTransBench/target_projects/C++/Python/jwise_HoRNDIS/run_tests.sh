#!/bin/bash
set -e
# Simple test runner: runs all pytest-based tests (original and public)
pip install -r requirements.txt
pytest tests/original
pytest public_tests