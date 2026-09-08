#!/bin/bash
# Run all public tests (those in the public_tests directory) with Jest and coverage
echo "Running Public Jest tests with coverage"
npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html