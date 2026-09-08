#!/bin/bash
# Run public polygon centroid tests with coverage using c8 (for ESM compatibility)
npx c8 --reporter=text --reporter=html mocha "public_tests/**/*.js"