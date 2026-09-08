#!/bin/bash
# Run only public tests (those ending with PublicTest.java)
# Use Maven's -Dtest syntax for pattern matching.

mvn -B -Dtest='*PublicTest' test