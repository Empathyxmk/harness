#!/bin/bash
set -e

# Only run tests on files that are actual tests, not setup.py or others
coverage run --branch -m pytest test_*.py
coverage report --show-missing