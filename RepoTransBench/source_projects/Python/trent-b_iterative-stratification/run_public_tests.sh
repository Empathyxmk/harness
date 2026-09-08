#!/bin/bash
# Run all public tests with coverage, including branch coverage, in the public_tests directory
coverage run --branch -m pytest public_tests/
coverage report --show-missing