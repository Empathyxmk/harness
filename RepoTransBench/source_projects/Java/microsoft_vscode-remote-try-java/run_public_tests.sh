#!/bin/bash
set -e
# Run only the public test class using Maven Surefire's -Dtest option.
mvn test -Dtest=AppPublicTest