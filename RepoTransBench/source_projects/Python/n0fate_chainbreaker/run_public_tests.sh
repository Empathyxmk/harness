#!/bin/bash
# Run all public tests with ensured PYTHONPATH so 'chainbreaker' package is available
PYTHONPATH=$(pwd) pytest --maxfail=1 --disable-warnings public_tests/