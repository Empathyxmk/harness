#!/bin/bash
coverage run --branch -m pytest tests/
RESULT=$?
coverage report --show-missing
coverage html
exit $RESULT