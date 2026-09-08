#!/bin/bash
# Run pytest with branch + line coverage for all source
coverage run --branch -m pytest
coverage report --show-missing
coverage html