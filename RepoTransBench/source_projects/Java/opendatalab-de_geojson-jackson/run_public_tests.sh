#!/bin/bash
set -e

# Compile and run only public tests (with "public_" prefix), skipping default ones if possible.
# This works because Maven surefire executes all *Test.java by default, but here we want only the public_* ones.
mvn -Dtest=public_* test