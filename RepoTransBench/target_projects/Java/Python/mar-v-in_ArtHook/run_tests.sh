#!/bin/bash
set -e
export PYTHONPATH=./src${PYTHONPATH:+:$PYTHONPATH}
pytest tests/original
pytest public_tests