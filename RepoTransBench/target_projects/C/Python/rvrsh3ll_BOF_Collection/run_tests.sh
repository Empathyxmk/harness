#!/bin/bash
set -e

echo "[*] Installing Python dependencies..."
pip install -r requirements.txt

echo "[*] Running all original and public tests..."
# Use pytest to discover and run all tests in the current directory and subdirectories
pytest --verbose