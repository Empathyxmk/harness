#!/bin/bash
# Run all tests with coverage, including branch coverage
pip install -r requirements.txt
pytest --cov=flask_jwt_extended --cov-report=term-missing --cov-report=html --cov-branch