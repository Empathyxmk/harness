#!/bin/bash
# Ensure the current script's directory is set as PYTHONPATH for test discovery
export PYTHONPATH=$(pwd)
echo "Running public tests with PYTHONPATH=$PYTHONPATH..."
pytest public_tests/