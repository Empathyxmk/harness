#!/bin/bash
pip install pytest coverage pytest-cov
coverage run --branch -m pytest
coverage report
coverage html