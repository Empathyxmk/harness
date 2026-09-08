#!/bin/bash
# Run all tests with coverage, including branch coverage
coverage erase
coverage run --branch -m pytest --maxfail=1 --disable-warnings
coverage report