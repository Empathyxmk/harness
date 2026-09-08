#!/bin/bash
set -e
npm install
npx mocha "public_tests/**/*.public.test.js"