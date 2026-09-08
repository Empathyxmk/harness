#!/bin/bash
set -e

# Install development requirements if present
if [ -f requirements-dev.txt ]; then
    pip install -r requirements-dev.txt
fi

pip install pytest pytest-cov tomli

COVARGS="--cov=pre_commit_hooks --cov-report=term-missing --cov-branch"
pytest $COVARGS tests