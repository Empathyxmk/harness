#!/bin/bash
# Run all tests with coverage (line and branch)
coverage run --branch -m pytest
coverage report
coverage html