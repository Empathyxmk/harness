#!/bin/bash
# Run all tests with coverage and branch metrics, show missing lines/branches
coverage erase
coverage run --branch -m unittest discover -s tests
coverage report -m --skip-covered