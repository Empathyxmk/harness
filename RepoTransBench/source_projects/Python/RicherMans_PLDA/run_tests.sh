#!/bin/bash
set -e

# Fix pip_install.txt for proper dependency installation
if [ -f pip_install.txt ]; then
    # Replace sklearn with scikit-learn before installation
    sed 's/^sklearn$/scikit-learn/' pip_install.txt > pip_install_fixed.txt
    pip install -r pip_install_fixed.txt
fi

# Set PYTHONPATH to find 'liblda' for tests
export PYTHONPATH=$(pwd)/python:$(pwd)/python/liblda:$PYTHONPATH

# Run all test scripts in the tests directory with coverage
coverage run --branch -m unittest discover -s tests -p "*.py"
coverage report --skip-covered
coverage html