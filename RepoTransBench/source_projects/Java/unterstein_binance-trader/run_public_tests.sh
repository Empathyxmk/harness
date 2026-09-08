#!/bin/bash
# Run only the public tests (those ending with PublicTest.java)
mvn -Dtest='*PublicTest' test