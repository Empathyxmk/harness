#!/bin/bash
set -e

npm install

if ! npx --no-install jest --version >/dev/null 2>&1 ; then
  npm install --save-dev jest
fi

npx jest --coverage --coverageReporters=text --coverageReporters=html