#!/bin/bash
# Run all tests with coverage, with branch coverage enabled
coverage run --branch -m pytest
coverage report