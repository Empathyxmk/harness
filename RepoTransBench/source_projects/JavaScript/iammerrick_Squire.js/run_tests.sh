#!/bin/bash
set -e

# Run jest with coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html