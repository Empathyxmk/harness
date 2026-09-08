#!/bin/bash
# Run all public tests with coverage
npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html