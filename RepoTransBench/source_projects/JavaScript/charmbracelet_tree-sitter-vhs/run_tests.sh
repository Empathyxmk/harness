#!/bin/bash
set -e
export NODE_OPTIONS="--experimental-vm-modules"
npx jest --coverage --coverageReporters=text --coverageReporters=html