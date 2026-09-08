#!/bin/bash
# Run all PUBLIC tests (with 'Public' in class name) using Maven from the project root

# Only run test classes containing 'Public' in their name
mvn -Dtest='**/*PublicTest' test