#!/bin/bash
set -e

pip install pytest coverage pytest-cov unittest-data-provider six requests

# Run coverage on both unit and integration-style (network) tests if possible
coverage run --branch -m pytest owncloud/test/
coverage report --show-missing