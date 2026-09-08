#!/bin/bash
# Remove pylama if installed, to avoid test plugin conflicts
pip uninstall -y pylama >/dev/null 2>&1
export PYTHONPATH=src
pytest tests/