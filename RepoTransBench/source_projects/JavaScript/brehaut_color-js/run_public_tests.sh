#!/bin/bash
npx nyc --reporter=text --reporter=html npx mocha public_tests/*.js