#!/bin/bash
set -e
export PYTHONPATH=.
coverage run --branch -m pytest --tb=short