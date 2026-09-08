#!/bin/bash
set -e
# Run Jest tests and collect coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html