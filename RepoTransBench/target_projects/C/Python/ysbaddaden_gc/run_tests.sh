#!/bin/bash
set -e

export PYTHONPATH=src

pytest tests/
pytest public_tests/