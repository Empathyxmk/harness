#!/bin/bash
set -e

# Use jest for running tests with coverage output
npx jest --coverage --coverageReporters=text --coverageReporters=html