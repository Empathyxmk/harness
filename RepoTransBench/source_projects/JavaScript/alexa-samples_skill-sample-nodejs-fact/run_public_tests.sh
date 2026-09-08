#!/bin/bash
cd lambda/custom
npx jest --config=__public__/jest.config.js --coverage --coverageReporters=text