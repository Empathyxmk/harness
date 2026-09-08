#!/bin/bash
# Run all public tests (those under src/test/java/com/yun/flogger/test/publics)

# Only compile and run tests in the publics folder.
mvn -Dtest=com.yun.flogger.test.publics.*Test test