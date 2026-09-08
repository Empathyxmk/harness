#!/bin/bash
echo "Running public tests with coverage..."
# Public tests run alongside the rest by Maven.
mvn test -Dtest='*PublicTest'