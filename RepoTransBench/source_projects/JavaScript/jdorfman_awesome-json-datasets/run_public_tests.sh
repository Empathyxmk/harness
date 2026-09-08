#!/bin/bash
set -e
npm install
npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html