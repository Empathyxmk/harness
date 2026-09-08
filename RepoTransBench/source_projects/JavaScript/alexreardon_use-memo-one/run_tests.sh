#!/bin/bash
set -e

# Run tests with coverage using jest (use npm instead of yarn)
npx jest --coverage --coverageReporters=text --coverageReporters=html