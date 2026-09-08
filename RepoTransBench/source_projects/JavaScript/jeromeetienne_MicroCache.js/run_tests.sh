#!/bin/bash
# Run Jest with coverage, focusing only on the 'tests' folder
npx jest --coverage --coverageReporters=text --coverageReporters=html tests