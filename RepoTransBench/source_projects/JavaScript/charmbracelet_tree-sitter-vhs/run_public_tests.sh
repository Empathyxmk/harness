#!/bin/bash
set -e
export NODE_OPTIONS="--experimental-vm-modules"
npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html