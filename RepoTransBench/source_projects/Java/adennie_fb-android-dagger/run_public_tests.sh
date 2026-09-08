#!/bin/bash
# Run ONLY public tests by invoking Maven, restricting to *PublicTest.java files

# Only run test classes that end with 'PublicTest' to ensure public tests are separate
mvn -Dtest='**/*PublicTest' test