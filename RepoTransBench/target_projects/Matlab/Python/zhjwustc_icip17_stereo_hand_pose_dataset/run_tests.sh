#!/bin/bash
set -e

echo "==== Running ALL tests (original and public) ===="
pytest

echo "==== Running only ORIGINAL tests ===="
pytest tests/original/

echo "==== Running only PUBLIC tests ===="
pytest public_tests/

echo "==== All Python tests completed ===="