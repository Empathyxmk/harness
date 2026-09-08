#!/bin/bash
export PYTHONPATH=$(pwd)/src
coverage run --branch -m pytest tests
CODE=$?
coverage report -m
exit $CODE