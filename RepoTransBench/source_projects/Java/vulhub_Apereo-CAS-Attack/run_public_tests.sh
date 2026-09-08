#!/bin/bash
set -e
# Only run public test file using Maven's includes filter
mvn -Dtest=org.vulhub.AppPublicTest test
mvn jacoco:report