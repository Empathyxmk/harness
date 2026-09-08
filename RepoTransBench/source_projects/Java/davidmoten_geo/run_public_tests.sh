#!/bin/bash
# Runs all *PublicTest.java tests for geo and geo-mem specifically
set -e
mvn -f geo/pom.xml -Dtest=*PublicTest test
mvn -f geo-mem/pom.xml -Dtest=*PublicTest test