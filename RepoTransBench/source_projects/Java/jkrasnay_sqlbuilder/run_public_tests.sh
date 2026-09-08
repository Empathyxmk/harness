#!/bin/bash
# Run only the public tests by Maven include pattern

set -e
# Use Maven's -Dtest=... pattern to only run *PublicTest classes
mvn --batch-mode -Dmaven.test.failure.ignore=false -Dtest="*PublicTest" test