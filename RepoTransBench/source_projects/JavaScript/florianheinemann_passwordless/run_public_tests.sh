#!/bin/bash
# Run all public tests with jest
npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html