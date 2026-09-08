#!/bin/bash
set -e

npm install

if ! npx --no-install jest --version >/dev/null 2>&1 ; then
  npm install --save-dev jest
fi

npx jest public_tests/ --coverage --coverageReporters=text --coverageReporters=html