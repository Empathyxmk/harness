#!/bin/bash
# This script runs only public test classes matching '*PublicTest.java', not jacoco
mvn -Dtest='*PublicTest' test