#!/bin/bash
set -e
export PYTHONPATH="$PYTHONPATH:$(pwd)/src"
pytest