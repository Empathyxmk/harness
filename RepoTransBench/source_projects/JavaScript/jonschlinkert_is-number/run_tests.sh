#!/bin/bash
npx nyc --reporter=text --reporter=html npx mocha test.js test/is-number.extra.test.js test/test-is-number-complete.js