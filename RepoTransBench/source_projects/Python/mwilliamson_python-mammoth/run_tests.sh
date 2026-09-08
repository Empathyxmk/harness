#!/bin/bash
# Run all Python tests with branch and line coverage
coverage run --branch -m pytest tests
coverage report --skip-covered
coverage html