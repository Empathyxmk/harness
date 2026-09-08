#!/bin/bash
set -e
mvn clean test
mvn jacoco:report