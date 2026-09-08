#!/bin/bash
set -e
# Use c8 for coverage for cross-tool compatibility
npx c8 --reporter=text --reporter=html npx jest --config=jest.config.js --passWithNoTests