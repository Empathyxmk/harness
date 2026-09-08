#!/bin/bash
set -e
MVN_BIN="mvn"
if ! command -v mvn >/dev/null 2>&1; then
  echo "Maven is required (mvn not found on PATH)" >&2
  exit 1
fi

echo "Building and running ALL (original + public) tests..."
$MVN_BIN clean test