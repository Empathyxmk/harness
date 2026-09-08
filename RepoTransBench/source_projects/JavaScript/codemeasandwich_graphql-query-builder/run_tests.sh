#!/bin/bash
npx nyc --reporter=text --reporter=html mocha test.js test-extra.js