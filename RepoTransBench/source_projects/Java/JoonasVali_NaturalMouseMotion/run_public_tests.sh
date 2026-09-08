#!/bin/bash
# Run all *PublicTest.java classes only
# This ensures that only the public tests are run.

# Clean to make sure test class list is rebuilt, then filter for *PublicTest classes.
mvn -Dtest=*PublicTest test