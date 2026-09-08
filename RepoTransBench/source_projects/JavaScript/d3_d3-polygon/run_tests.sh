#!/bin/bash
# Run tests with coverage using c8 (for ESM compatibility)
npx c8 --reporter=text --reporter=html mocha "test/**/*.js"