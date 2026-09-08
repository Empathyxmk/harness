#!/bin/bash
# Run all public tests in the public_tests/ directory using unittest (not pytest) to avoid pylama/plugin issues
python3 -m unittest discover -s public_tests -p "test_*.py"