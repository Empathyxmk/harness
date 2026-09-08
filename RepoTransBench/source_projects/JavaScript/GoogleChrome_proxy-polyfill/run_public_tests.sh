#!/bin/bash
set -e

export NODE_ENV=test
npx nyc --reporter=text --reporter=html mocha public_tests/proxy_polyfill.edge.public.test.js