#!/bin/bash
set -e

echo "Cleaning target directory ... "
cargo clean

# Ensure data subdir exists for test_fastq_io test
mkdir -p tests/data
cp test/test.fastq tests/data/test.fastq

echo "Building and running all tests ..."
cargo test --all -- --nocapture

echo "All tests executed."