#!/bin/bash
set -e

# Run all tests under both original and public
pytest tests/original/
pytest public_tests/