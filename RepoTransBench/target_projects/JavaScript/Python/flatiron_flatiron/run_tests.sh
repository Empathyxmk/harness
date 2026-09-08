#!/bin/bash
set -e

# Run all tests: both original and public tests.
pytest --maxfail=3 --disable-warnings