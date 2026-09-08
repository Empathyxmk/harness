#!/bin/bash
# Runs all existing tests for geo and geo-mem (with test reports)
set -e
mvn -f geo/pom.xml test
mvn -f geo-mem/pom.xml test