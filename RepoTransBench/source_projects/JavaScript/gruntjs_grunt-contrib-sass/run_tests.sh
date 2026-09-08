#!/bin/bash
# Modern test script for Jest + coverage
echo "Running Jest tests with coverage"
npx jest --coverage --coverageReporters=text --coverageReporters=html