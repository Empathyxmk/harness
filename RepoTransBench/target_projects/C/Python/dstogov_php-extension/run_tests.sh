#!/bin/bash
set -e

# Run all tests with pytest
python -m pytest tests/ public_tests/ -v