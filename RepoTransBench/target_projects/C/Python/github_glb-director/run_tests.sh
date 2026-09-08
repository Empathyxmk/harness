#!/bin/bash
set -e

# Run both original and public tests using pytest
python -m pytest tests/original/ public_tests/ -v