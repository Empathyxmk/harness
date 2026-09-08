#!/bin/bash
set -e
PYTHONPATH=$(pwd)
export PYTHONPATH
pytest tests/original/ public_tests/