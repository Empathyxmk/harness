#!/bin/bash
set -e

export NODE_ENV=test
npx nyc --reporter=text --reporter=html mocha test.js test/proxy_polyfill.edge.test.js