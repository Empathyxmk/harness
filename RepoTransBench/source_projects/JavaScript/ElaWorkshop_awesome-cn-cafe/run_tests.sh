#!/bin/bash
cd tools
npx jest --coverage --coverageReporters=text --coverageReporters=html
cd ..