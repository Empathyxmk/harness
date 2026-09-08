#!/bin/bash
set -e

# Install dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

pip install pytest pytest-asyncio pytest-cov coverage

# Compile Cython files if needed
if [ -f jd4/_compare.pyx ] || [ -f jd4/_sandbox.pyx ]; then
    pip install cython
    python setup.py build_ext --inplace
fi

export PYTHONPATH=$(pwd)

# Run all tests with coverage (line+branch)
coverage run --branch -m pytest jd4/
coverage report -m