#!/bin/bash
set -e
echo "==== Running Python Unit and Public Tests (pytest) ===="
pytest tests/original
pytest public_tests
pytest