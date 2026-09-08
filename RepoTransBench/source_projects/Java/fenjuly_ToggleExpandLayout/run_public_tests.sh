#!/bin/bash
cd library

# Run only the public tests we created (those ending with PublicTest in the test directory).
../gradlew clean testDebugUnitTest --tests '*PublicTest'

echo "=== Ran public tests only (matching '*PublicTest') ==="