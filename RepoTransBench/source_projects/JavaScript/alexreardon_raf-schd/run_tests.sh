#!/bin/bash
set -e

# Run all tests with coverage using Jest
npx jest --coverage --coverageReporters=text --coverageReporters=html