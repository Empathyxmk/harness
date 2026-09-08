#!/bin/bash
set -e

# Run jest only for public tests
npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html