#!/bin/bash
# Run ONLY public test class(es) using Maven Surefire's -Dtest
echo "Running public tests only..."
mvn -Dtest=Log4jPublicTest test