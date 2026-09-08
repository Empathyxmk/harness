#!/bin/bash
set -e
export PYTHONPATH=$(pwd)/src:$PYTHONPATH
pytest