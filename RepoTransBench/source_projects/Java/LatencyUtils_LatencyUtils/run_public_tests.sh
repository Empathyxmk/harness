#!/bin/bash
# Run only *PublicTest.java classes, for public test validation with Maven
mvn -Dtest='*PublicTest' test