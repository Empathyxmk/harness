#!/bin/bash
set -e

# Run tests in all Maven modules (root, annotation, processor, bundler-parceler)
mvn test