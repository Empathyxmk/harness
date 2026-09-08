#!/bin/bash
set -e

pip install pytest coverage pytest-cov "pydantic[dotenv]>=1.8" hypothesis

coverage run --branch -m pytest --disable-warnings -q
coverage report -m --skip-covered || true
coverage html