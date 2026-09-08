#!/bin/bash
set -e

echo "Running public test scalars"
node public_tests/scalars.public.js

echo "Running public test validation"
node public_tests/validation.public.js

echo "Running public test json"
node public_tests/json.public.js

echo "Running public test keys"
node public_tests/keys.public.js