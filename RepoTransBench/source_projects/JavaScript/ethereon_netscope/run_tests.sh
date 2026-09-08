#!/bin/bash
set -e

# CoffeeScript tests (existing)
npx mocha --require coffee-script/register "test/**/*.coffee"

# JS/Node tests for AppController/netscope.js
npx nyc --reporter=text --reporter=html npx mocha "test/**/*.js"