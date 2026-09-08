#!/bin/bash
echo "Running public tests..."
# Ensure only *_PublicTest.java are picked up if public tests need separation
# But as per Java/IDEA/Maven defaults, all *Test.java are run. To only run public tests, use includes.
mvn -Dtest=**/*PublicTest test