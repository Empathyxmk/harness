#!/bin/bash
cd "$(dirname "$0")"
./mvnw test jacoco:report