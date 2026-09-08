#!/bin/bash
set -e

# Run all tests (original + public)
pytest tests/ tests/original/ public_tests/