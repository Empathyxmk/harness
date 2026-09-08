#!/bin/bash
# Run only public test classes (those with 'PublicTest' or 'ExamplePublicUnitTest' in their name).
# This script assumes Gradle is the build tool.
./gradlew test --tests '*PublicTest' --tests '*ExamplePublicUnitTest*'