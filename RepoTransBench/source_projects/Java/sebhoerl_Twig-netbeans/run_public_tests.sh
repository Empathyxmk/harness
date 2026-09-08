#!/bin/bash
# Runs ONLY public tests for the org.netbeans.modules.php.twig.editor package and subpackages

cd "$(dirname "$0")/twig-netbeans" || exit 1

# Only execute *PublicTest classes
mvn -Dtest='**/*PublicTest' test