#!/bin/bash
set -e

# Install dependencies if needed
pip install --upgrade pip
pip install poetry pytest pytest-cov httpx fastapi tiktoken

# Install project dependencies
if [ -f "pyproject.toml" ]; then
    poetry install
fi

# Run only public tests
pytest public_tests/