#!/bin/bash
set -e

# Install dependencies
npm install

# Run only public tests
npx jest public_tests/