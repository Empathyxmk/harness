#!/bin/bash
set -e

# Install dependencies if needed
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

pytest