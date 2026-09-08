#!/bin/bash
# Runs only the public tests with names *PublicTest.java

cd dexplore-lib
./../gradlew test --tests "*PublicTest"