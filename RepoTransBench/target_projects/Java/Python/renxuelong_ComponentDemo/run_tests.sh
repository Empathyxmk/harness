#!/bin/bash
set -e

# Install requirements if needed (optional for user, but suggested)
# pip install -r requirements.txt

pytest --maxfail=3 --disable-warnings -v