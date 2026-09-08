#!/bin/bash
set -e

# Build and test only the dearbinge-openapi module, restricting to *PublicTest classes
mvn clean test -pl dearbinge-openapi -Dtest=*PublicTest

echo "Public tests for dearbinge-openapi executed."