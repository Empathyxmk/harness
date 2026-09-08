#!/bin/bash
set -e

echo "Running public tests..."
mvn -Dtest=adp.pathmorph.PlayToPauseMorphPublicTest,adp.pathmorph.PlayToPauseMorphAdditionalPublicTest test