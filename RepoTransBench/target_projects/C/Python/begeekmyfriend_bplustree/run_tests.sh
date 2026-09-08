#!/bin/bash
set -e

# Install dependencies if not already present
pip install -r requirements.txt

# Run ALL tests (original and public)
pytest