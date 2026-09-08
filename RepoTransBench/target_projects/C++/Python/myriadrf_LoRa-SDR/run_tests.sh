#!/bin/bash
set -e

# Execute both original and public Python test suites using pytest
pytest tests/original/ public_tests/