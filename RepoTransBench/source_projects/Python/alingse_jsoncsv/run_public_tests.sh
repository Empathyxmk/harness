#!/bin/bash
# This script runs all public tests with proper PYTHONPATH so 'jsoncsv' is found.

PYTHONPATH=$(pwd) pytest public_tests/