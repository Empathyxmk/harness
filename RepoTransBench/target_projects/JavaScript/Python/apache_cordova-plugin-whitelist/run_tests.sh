#!/bin/bash
set -e

# Install requirements if needed
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

pytest