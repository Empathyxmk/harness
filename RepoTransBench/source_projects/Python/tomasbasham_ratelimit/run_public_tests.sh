#!/bin/bash
set -e
export PATH="/usr/local/bin:$PATH"
# Ensure correct pytest version, prefer system path
which pytest || export PATH="$HOME/.local/bin:$PATH"
echo "Python version:"
python --version
echo "Pytest version:"
pytest --version
pip install -r requirements.txt  # just in case
pytest --tb=short --maxfail=1 public_tests/