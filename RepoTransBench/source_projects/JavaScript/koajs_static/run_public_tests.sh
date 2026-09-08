#!/bin/bash
# Run all public tests located in the public_tests directory
npx jest public_tests --coverage --coverageReporters=text --coverageReporters=html