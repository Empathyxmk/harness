#!/bin/bash
export PATH="./node_modules/.bin:$PATH"
nyc --reporter=text --reporter=html mocha "public_tests/**/*.js"