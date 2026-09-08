#!/bin/bash
# Run all .js tests in test/ with coverage using mocha (CommonJS compatible)
export NODE_ENV=test
npx nyc --reporter=text --reporter=html npx mocha "test/**/*.js"