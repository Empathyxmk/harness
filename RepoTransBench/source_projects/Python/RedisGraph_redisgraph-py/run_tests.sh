#!/bin/bash
set -e
export PYTHONPATH=$(pwd)
coverage run --branch -m pytest tests/unit
coverage report -m
coverage html