#!/bin/bash
# Script to run all public tests ONLY

# Use Maven to run only FileManagerPublicTest (public tests)
mvn -Dtest=com.github.filemanager.FileManagerPublicTest test

if [ $? -eq 0 ]; then
  echo "Public tests ran successfully."
else
  echo "Public test failure or error."
  exit 1
fi