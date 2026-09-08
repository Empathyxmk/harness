#!/bin/bash
set -e
# Run only public tests, by convention any file named public_test_*.py
coverage erase
coverage run --branch -m unittest discover -s . -p "public_test_*.py"
coverage report
coverage html

exit $?