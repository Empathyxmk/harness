#!/bin/bash
# Run all public tests using jest

npx jest --coverage --coverageReporters=text --coverageReporters=html public_tests/