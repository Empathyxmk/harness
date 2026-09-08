#!/bin/bash
set -e

# Only run *PublicTest.java files for public test coverage (Java 1.7)
mvn -Dtest='**/*PublicTest.java' test -Dmaven.compiler.source=1.7 -Dmaven.compiler.target=1.7

echo "Public tests complete."