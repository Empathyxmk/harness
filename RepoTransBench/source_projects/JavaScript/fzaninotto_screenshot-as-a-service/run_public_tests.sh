#!/bin/bash
# Run only public test files in ./public_tests with Jest
npx jest public_tests/ --runInBand --detectOpenHandles