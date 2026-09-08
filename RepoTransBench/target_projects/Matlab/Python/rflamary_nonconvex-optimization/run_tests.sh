#!/bin/bash
set -e

# Activate venv, if exists
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi

pytest