#!/bin/bash
# Run all tests with coverage, including branch coverage. Ensures correct PYTHONPATH for src import style.
export PYTHONPATH=$(pwd)
pytest --cov=chainbreaker --cov-report=term-missing --cov-report=html --cov-branch