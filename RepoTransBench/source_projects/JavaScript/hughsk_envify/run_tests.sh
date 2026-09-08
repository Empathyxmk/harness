#!/bin/bash
# Use Jest only for JS files outside node_modules, skip tape-based test.js
npx jest --coverage --coverageReporters=text --coverageReporters=html