#!/bin/bash
# Run only public tests (those named *PublicTest.java)
cd app
../gradlew test --tests '*PublicTest'
cd ..