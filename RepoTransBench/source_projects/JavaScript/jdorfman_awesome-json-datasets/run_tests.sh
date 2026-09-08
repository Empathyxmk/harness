#!/bin/bash
set -e
npm install
npx jest --coverage --coverageReporters=text --coverageReporters=html