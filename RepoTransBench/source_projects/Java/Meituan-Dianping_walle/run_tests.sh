#!/bin/bash
set -e
cd payload_reader
./gradlew clean test jacocoTestReport