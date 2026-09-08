#!/bin/bash
# Script to run all public tests

set -e

npm install

npx jest public_tests/ --coverage=false