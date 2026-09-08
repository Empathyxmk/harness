#!/bin/bash
# Run only supported tests with coverage, skipping test/test.js (causes error due to unmocked browser env)
npx jest --coverage --coverageReporters=text --coverageReporters=html test/index.test.js test/test.patch.js