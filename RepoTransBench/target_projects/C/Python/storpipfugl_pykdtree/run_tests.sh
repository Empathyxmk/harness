#!/bin/bash
set -e
export PYTHONWARNINGS="ignore"
pytest --maxfail=5 --disable-warnings pykdtree