#!/bin/bash
# Run all Jest public tests in the public_tests/ directory with coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html public_tests/