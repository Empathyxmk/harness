#!/bin/bash
set -e
export PYTHONPATH=.
coverage run --branch -m unittest discover siesta/tests
coverage report --show-missing