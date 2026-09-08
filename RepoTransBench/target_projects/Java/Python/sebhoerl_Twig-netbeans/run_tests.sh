#!/bin/bash
set -e

# Simple script to run all Python tests using pytest for both original and public tests.

pytest tests/original
pytest public_tests