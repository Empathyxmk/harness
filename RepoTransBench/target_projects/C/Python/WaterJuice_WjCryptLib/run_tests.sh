#!/bin/bash
# Simple test execution script for WjCryptLib Python port

# Exit on any error
set -e

# Make sure dependencies are installed
pip install -r requirements.txt

# Run all tests
pytest