#!/bin/bash
# Run only the public tests in the 'lib' module (by test class name)
./gradlew :lib:test --tests "*LoadingButtonPublicTest" --no-daemon