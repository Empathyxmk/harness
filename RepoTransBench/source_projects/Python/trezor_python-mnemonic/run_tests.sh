#!/bin/bash
pip install -q pytest coverage pytest-cov
export PYTHONPATH=src
coverage run --branch -m pytest tests
coverage report --show-missing --skip-covered