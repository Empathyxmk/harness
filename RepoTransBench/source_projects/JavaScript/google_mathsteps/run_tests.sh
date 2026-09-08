#!/bin/bash
set -e

# Install dependencies
npm install

# Run tests with coverage
npx jest --coverage