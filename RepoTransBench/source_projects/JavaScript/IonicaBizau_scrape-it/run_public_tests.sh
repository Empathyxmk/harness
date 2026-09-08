#!/bin/bash
set -e

# Run all public tests (using .public.spec.js) with Jest directly
npx jest test/public/*.public.spec.js