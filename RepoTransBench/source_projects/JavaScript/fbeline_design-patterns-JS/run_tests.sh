#!/bin/bash
# Run all JavaScript tests using jest, with coverage

set -e

npx jest --coverage --coverageReporters=text --coverageReporters=html