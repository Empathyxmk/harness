#!/bin/bash
# Run only *_PublicTest.java classes in dearbinge-openapi
cd "$(dirname "$0")"
mvn -Dtest=*PublicTest test