#!/bin/bash
set -e

if [ -x ./node_modules/.bin/jest ]; then
  ./node_modules/.bin/jest public_tests --coverage=false
else
  npx jest public_tests --coverage=false
fi