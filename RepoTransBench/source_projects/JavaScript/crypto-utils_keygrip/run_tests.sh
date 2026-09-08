#!/bin/bash
# Use mocha for test running with c8 coverage
npx c8 --reporter=text --reporter=html npx mocha "test/**/*.js"