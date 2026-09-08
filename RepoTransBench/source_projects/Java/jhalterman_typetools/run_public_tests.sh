#!/bin/bash
# Runs all Java public tests using Maven
set -e

# Only public tests matching *PublicTest.java pattern
mvn -Dtest='**/*PublicTest.java' test