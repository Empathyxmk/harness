#!/bin/bash
# Run all public tests in the project with pytest, for files in public_tests/
pip install pytest coverage pytest-cov pydantic hypothesis --quiet
pytest --maxfail=1 --disable-warnings --tb=short public_tests/