#!/bin/bash
set -e
# Only run *PublicTest and *PublicTest classes to avoid duplicate test data with private ones.
mvn -B -Dtest='*PublicTest' test