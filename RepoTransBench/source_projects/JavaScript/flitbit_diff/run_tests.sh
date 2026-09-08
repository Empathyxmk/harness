#!/bin/bash
set -e

# Run Jest and produce text & html coverage
npx jest --coverage --coverageReporters=text --coverageReporters=html