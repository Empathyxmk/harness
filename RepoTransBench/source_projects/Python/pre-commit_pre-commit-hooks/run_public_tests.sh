#!/bin/bash
# Script to run all public tests
export PATH="$HOME/.local/bin:$PATH"
python3 -m pytest public_tests/