#!/bin/bash
set -e

pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
pip install pytest coverage pytest-cov invoke dktasklib

# Use python -m coverage (for Python 3.11+ compatibility)
python3 -m coverage run --branch --source=pydeps,tasks,setup -m pytest --maxfail=1 --disable-warnings -v
python3 -m coverage report
python3 -m coverage html