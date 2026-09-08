#!/bin/bash
set -e

if ! command -v pytest &>/dev/null; then
    pip install -r requirements.txt
fi

python -m pytest tests/original
python -m pytest public_tests