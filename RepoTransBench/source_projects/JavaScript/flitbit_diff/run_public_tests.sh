#!/bin/bash
set -e

# Run only the public tests and produce text & html coverage
npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html