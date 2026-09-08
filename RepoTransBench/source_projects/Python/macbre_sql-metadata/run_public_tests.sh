#!/bin/bash
set -e

if command -v poetry &> /dev/null; then
    poetry install
    poetry run pytest public_tests/
else
    pip install -U pip
    pip install pytest sqlparse
    pytest public_tests/
fi