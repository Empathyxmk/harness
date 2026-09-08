#!/bin/bash
# Run only PublicTest* and *PublicTest.java classes as public tests
mvn -Dtest='**/*PublicTest' test