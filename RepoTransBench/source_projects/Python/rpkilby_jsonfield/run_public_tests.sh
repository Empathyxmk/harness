#!/bin/bash
# Script to run all public tests using pytest
pip install -e . --quiet
pip install pytest --quiet
pytest public_tests/ --tb=short -q