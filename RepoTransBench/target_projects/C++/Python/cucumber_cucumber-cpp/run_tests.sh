#!/bin/bash
set -e

# Ensure dependencies are installed
pip install -r requirements.txt

# Run all tests
pytest