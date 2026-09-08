#!/bin/bash
set -e

pip install -r base_requirements.txt
pip install flask pytest coverage pytest-cov tenacity requests

coverage run --branch -m pytest
coverage report
coverage html