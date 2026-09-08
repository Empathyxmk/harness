#!/bin/bash
# Run all tests with coverage, including branch coverage
coverage run --branch -m pytest
coverage report --show-missing