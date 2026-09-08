#!/bin/bash
set -e
pytest tests/ --maxfail=1 --disable-warnings
pytest public_tests/ --maxfail=1 --disable-warnings