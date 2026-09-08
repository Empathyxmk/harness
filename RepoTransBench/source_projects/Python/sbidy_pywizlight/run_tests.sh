#!/bin/bash
set -e

# Install pytest and pytest-asyncio if not available
python -c "import pytest" 2>/dev/null || pip install pytest
python -c "import pytest_asyncio" 2>/dev/null || pip install pytest-asyncio

# Run tests with coverage, including async support
coverage run --branch -m pytest --asyncio-mode=auto pywizlight/tests
coverage report