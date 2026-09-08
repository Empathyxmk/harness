#!/bin/bash
# Run all public tests using unittest discovery in the public_tests directory
python3 -m unittest discover -s public_tests -p "test_public_*.py"