#!/bin/bash
set -e
export PYTHONPATH=.
coverage run --branch -m pytest tests/
coverage report -m