#!/bin/bash
# Run ONLY public tests in the public_tests directory
npx jest --testMatch="**/public_tests/**/*.public.test.js"