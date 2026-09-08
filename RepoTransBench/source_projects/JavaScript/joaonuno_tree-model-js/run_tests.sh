#!/bin/bash
# Run all JS tests with coverage and show summary
npx nyc --reporter=text --reporter=html npx mocha "test/*.js"