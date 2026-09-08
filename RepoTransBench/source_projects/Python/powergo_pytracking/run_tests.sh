#!/bin/bash
set -e
pip install pytest coverage pytest-cov
coverage run --branch -m pytest tests
coverage report