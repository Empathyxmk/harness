#!/bin/bash
# Run all PrettyTime public tests for core and jsf modules

echo "Running public tests for all appropriate submodules..."

if [ -f ./core/pom.xml ]; then
  mvn -f ./core/pom.xml -Dtest=*PublicTest test || exit 1
fi
if [ -f ./jsf/pom.xml ]; then
  mvn -f ./jsf/pom.xml -Dtest=*PublicTest test || exit 1
fi