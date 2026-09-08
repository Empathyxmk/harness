#!/bin/bash
# Run all composite public tests only (filter by PublicTest naming pattern for public tests)
cd composite
mvn -Dtest='**/*PublicTest.java' test