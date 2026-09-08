#!/bin/bash
# Run only public tests (matching *PublicTest.java) for the payload_reader module

cd "$(dirname "$0")"

chmod +x ./gradlew
./gradlew test --tests '*PublicTest*'