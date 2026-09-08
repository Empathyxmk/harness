#!/bin/bash
set -e

npm install

# Only run files in the public_tests directory
npx jest public_tests --coverage