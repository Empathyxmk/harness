#!/bin/bash
set -e

pip install pytest coverage pytest-cov

COV_REPORT="--cov=configs/mv2d/exp --cov=configs/mv2d/data --cov-report=term-missing --cov-report=html --cov-branch"

echo "Discovering and running all pytest-based tests with coverage..."
pytest $COV_REPORT tests/