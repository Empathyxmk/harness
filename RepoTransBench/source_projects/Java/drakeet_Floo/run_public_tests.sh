#!/bin/bash
# Run only public tests (those files suffixed with PublicTest.java)
./gradlew test --tests '*PublicTest'