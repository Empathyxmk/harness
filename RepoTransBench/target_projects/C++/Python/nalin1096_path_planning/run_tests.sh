#!/bin/bash
set -e
# Run both original and public tests with pytest
pytest tests/
pytest public_tests/