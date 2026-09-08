#!/bin/bash
# Ensure module source root is in PYTHONPATH for imports
PYTHONPATH=$(pwd) pytest public_tests/