#!/bin/bash
set -e

coverage run --branch -m unittest discover -s public_tests -p "test_public_*.py"
coverage report -m