#!/bin/bash
set -e
pip install -r tests/requirements.txt || true
pytest tests/