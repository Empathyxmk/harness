#!/bin/bash
set -e

echo "Running Python pytest for all tests"
pytest --maxfail=3 --disable-warnings -v

echo "All tests passed!"