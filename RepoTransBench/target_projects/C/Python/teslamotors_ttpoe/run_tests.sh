#!/bin/bash
set -e
# Simple script to run all Python tests (original and public)
# Usage: ./run_tests.sh

pip install -r requirements.txt
pytest tests/original
pytest public_tests