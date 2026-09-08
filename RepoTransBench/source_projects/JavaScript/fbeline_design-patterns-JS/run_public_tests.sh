#!/bin/bash
# Run all JavaScript public tests in public_tests directory using jest

set -e

npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html