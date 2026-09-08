#!/bin/bash
set -e

pip install pytest coverage pytest-cov six
coverage run --branch -m pytest tests/
coverage report -m