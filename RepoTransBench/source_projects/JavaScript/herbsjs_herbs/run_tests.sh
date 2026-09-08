#!/bin/bash
set -e
npx nyc --reporter=text --reporter=html mocha test/