#!/bin/bash
pip install .
pip install pytest pytest-cov
pytest --cov=shortuuid --cov-branch --cov-report=term-missing --cov-report=html