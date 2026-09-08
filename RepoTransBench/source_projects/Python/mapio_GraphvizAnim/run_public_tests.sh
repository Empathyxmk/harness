#!/bin/bash
set -e

# Install dependencies from binder/requirements.txt if present
if [ -f binder/requirements.txt ]; then
    pip install -r binder/requirements.txt
fi

pip install pytest pytest-timeout

pytest public_tests/ --timeout=10