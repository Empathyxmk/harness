#!/bin/bash
# Run only public tests in badges module
./gradlew :badges:testDebugUnitTest --tests '*PublicTest'