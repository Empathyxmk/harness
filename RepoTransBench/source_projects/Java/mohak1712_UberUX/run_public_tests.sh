#!/bin/bash
cd app
./gradlew clean testDebugUnitTest --tests '*PublicTest' --info