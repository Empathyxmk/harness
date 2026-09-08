#!/bin/bash
# Run all public tests using pytest and print output

set -e
pytest public_tests/ "$@"