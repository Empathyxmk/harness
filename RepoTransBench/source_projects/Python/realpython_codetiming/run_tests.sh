#!/bin/bash
export PYTHONPATH=.
coverage run --branch -m pytest --tb=short --disable-warnings
STATUS=$?
coverage report
coverage html
exit $STATUS