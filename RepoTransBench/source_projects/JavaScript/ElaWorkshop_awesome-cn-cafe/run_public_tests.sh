#!/bin/bash
# Run all public test files in tools/ ending with .public.test.js
cd tools
npx jest --testPathPatterns="public\\.test\\.js$"