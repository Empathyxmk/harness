#!/bin/bash
# Run all public JS tests for joaonuno_tree-model-js (public only)
npx nyc --reporter=text --reporter=html npx mocha "public_tests/*.js"