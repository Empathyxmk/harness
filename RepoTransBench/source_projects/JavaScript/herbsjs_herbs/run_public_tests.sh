#!/bin/bash
# Script to run all public tests in the public_tests directory using mocha
if [ -d "./public_tests" ]; then
  npx mocha "./public_tests/*.js"
else
  echo "No public_tests directory found!"
  exit 1
fi