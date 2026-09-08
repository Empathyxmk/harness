#!/bin/bash
export NODE_OPTIONS="--experimental-vm-modules"
npx jest public_tests/ --config=jest.config.js --coverage=false