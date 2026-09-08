#!/bin/bash
set -e

# Only run public test classes (those ending with PublicTest)
./mvnw -Dtest='*PublicTest' test

echo "Public tests run completed."