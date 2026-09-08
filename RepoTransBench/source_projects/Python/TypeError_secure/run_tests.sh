#!/bin/bash
# Ensure the secure package is on PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH
echo "Running pytest with coverage..."
pytest --cov=secure --cov-report=term-missing --cov-report=html --cov-branch