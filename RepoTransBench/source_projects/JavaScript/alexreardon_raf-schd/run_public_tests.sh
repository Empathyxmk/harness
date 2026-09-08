#!/bin/bash
set -e

# Run all public tests with coverage using Jest
npx jest --coverage --coverageReporters=text --coverageReporters=html public_tests/