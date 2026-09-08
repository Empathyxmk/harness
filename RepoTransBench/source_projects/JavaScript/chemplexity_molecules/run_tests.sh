#!/bin/bash
export NODE_OPTIONS="--experimental-vm-modules"
npx jest --config=jest.config.js --coverage --coverageReporters=text --coverageReporters=html