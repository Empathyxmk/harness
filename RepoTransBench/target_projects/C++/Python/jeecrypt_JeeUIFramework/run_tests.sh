#!/bin/bash
set -e
# Simple test runner for all tests (original + public)
PYTHONPATH=src pytest tests/ public_tests/