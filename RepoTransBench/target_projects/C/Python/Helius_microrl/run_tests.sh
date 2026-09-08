#!/bin/bash
set -e

echo "[*] Installing Python dependencies..."
pip install -r requirements.txt

echo "[*] Running all tests (original and public)..."
# pytest automatically discovers tests in directories named 'test_*' or files named 'test_*.py'
# from the current working directory.
# This command will find tests in tests/original/ and tests/public/.
pytest

echo "[*] All tests completed."