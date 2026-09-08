#!/bin/bash
cd lambda/custom
npx jest --config=jest.config.js --coverage --coverageReporters=text --coverageReporters=html