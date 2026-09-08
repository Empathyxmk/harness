#!/bin/bash
# Run all public tests with coverage (line and branch)
coverage run --branch -m pytest public_tests/
coverage report
coverage html -d htmlcov_public