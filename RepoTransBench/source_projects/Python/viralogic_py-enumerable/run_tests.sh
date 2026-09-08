#!/bin/bash
set -e
pip install pytest coverage pytest-cov
pytest --maxfail=1 --disable-warnings -q tests