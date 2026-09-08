#!/bin/bash
# Run only public tests with Maven Surefire includes

mvn -Dtest='*PublicTest' test
EXIT_CODE=$?
echo "Public test classes in src/test/java with '*PublicTest.java'"
exit $EXIT_CODE