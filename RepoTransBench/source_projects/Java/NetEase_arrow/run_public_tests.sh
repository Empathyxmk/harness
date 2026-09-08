#!/bin/bash
# Run only public tests using Maven
# This includes only *PublicTest.java files, using the Maven "test" phase and the -Dtest pattern for clarity.
mvn -Dtest='*PublicTest' test