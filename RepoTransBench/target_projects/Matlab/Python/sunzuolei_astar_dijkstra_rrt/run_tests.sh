#!/bin/bash
set -e
echo "=== Installing dependencies ==="
pip install -r requirements.txt
echo "=== Running all Python tests ==="
pytest tests/ tests/original/ public_tests/ --maxfail=5 --disable-warnings -v