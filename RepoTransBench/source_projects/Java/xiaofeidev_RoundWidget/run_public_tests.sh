#!/bin/bash
cd lib_round
./gradlew clean testDebugUnitTest --tests '*PublicTest'
cd ..