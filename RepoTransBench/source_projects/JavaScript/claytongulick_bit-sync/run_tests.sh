#!/bin/bash
set -e
# Run jest tests with coverage reporting (text and HTML)
npx jest --coverage --coverageReporters=text --coverageReporters=html "$@"