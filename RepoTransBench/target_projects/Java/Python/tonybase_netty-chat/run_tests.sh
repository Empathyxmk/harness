#!/bin/bash
set -e
pip install -r requirements.txt
pytest tests/original/
pytest public_tests/