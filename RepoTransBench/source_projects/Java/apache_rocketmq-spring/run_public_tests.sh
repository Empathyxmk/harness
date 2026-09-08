#!/bin/bash
set -e

# Only run public tests (using class pattern '*PublicTest')
# This will run in all submodules, and the test includes only *PublicTest.java
mvn -B -Dtest=*PublicTest test

echo "Completed public tests. Only '*PublicTest' classes were executed."