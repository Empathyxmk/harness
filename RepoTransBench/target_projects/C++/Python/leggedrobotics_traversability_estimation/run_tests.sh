#!/bin/bash
set -e
export PYTHONPATH=src
pytest "$@"