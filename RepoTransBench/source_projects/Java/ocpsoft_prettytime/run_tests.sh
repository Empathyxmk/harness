#!/bin/bash
# Run all core and jsf PrettyTime tests, ignore coverage if plugins missing

echo "Running all PrettyTime tests..."
if [ -f ./core/pom.xml ]; then
  mvn -f ./core/pom.xml test || exit 1
fi
if [ -f ./jsf/pom.xml ]; then
  mvn -f ./jsf/pom.xml test || exit 1
fi