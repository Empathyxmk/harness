#!/bin/bash
# Run only public tests (public_tests directory, all *.public.test.js files)
npx jest --coverage --coverageReporters=text --coverageReporters=html public_tests/