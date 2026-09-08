#!/bin/bash
set -e

pip install -r requirements.txt
pip install pytest coverage pytest-cov pandas requests

coverage run --branch -m pytest tests
coverage report
coverage html