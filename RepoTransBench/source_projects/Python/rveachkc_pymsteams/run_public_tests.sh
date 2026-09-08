#!/bin/bash
pip install pytest --quiet
echo "Running public tests..."
pytest public_tests/