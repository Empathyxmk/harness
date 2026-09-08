#!/bin/bash
set -e

export NODE_ENV=test

# Run only public Jest tests in public_tests directory
npx jest public_tests/ --runInBand