#!/bin/bash
# Public test script for brettwooldridge_SansOrm

set -e
mvn -Dtest=**/*PublicTest.java test