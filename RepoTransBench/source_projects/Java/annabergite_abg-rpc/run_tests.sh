#!/bin/bash
# Run all tests for all modules, skip signing, skip javadoc, tests only
mvn -Dgpg.skip=true -Dmaven.javadoc.skip=true test