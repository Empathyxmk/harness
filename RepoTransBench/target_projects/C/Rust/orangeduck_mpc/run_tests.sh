#!/bin/bash
set -e

# Run all tests in the project
echo "Running all tests..."
cargo test

# To run only the original tests
# cargo test --test core_tests --test regex_tests --test grammar_tests --test combinators_tests

# To run only the public tests
# cargo test --test test_public --test core_public --test regex_public --test grammar_public --test combinators_public

echo "All tests completed!"