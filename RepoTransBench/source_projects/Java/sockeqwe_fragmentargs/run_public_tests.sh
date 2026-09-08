#!/bin/bash
set -e
cd annotation
# Only run *PublicTest.java
mvn -Dtest=*PublicTest test
cd ..
cd processor
# Only run *PublicTest.java
mvn -Dtest=*PublicTest test