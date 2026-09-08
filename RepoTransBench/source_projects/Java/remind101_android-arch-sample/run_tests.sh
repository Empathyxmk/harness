#!/bin/bash
# Run all unit tests (including public and non-public)
cd app
../gradlew test
cd ..