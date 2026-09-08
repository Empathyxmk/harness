#!/bin/bash
# Run all public tests from the project root using correct PYTHONPATH
PYTHONPATH=$(pwd) pytest public_tests