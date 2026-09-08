#!/bin/bash
set -e

# Run only the public tests using Maven (by classname pattern)
mvn -Dtest=io.herrmann.generator.GeneratorPublicTest test