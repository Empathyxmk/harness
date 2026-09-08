#!/bin/bash
set -e

# Make src/csvquote_wrapper a discoverable package
python3 -c "import os; os.makedirs('src/csvquote_wrapper', exist_ok=True)"
python3 -c "open('src/__init__.py', 'a').close()"
python3 -c "open('src/csvquote_wrapper/__init__.py', 'a').close()"
python3 -c "open('tests/__init__.py', 'a').close()"
python3 -c "open('tests/original/__init__.py', 'a').close()"
python3 -c "open('public_tests/__init__.py', 'a').close()"

# Build the C executable
python3 -c "from src.csvquote_wrapper.csvquote_cli import build_csvquote; build_csvquote()"

# Run all tests using pytest
pytest

echo "All tests passed."