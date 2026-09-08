#!/bin/bash
set -e

# Run only public tests
echo "Running public tests..."
cargo test --test test_public --test core_public --test regex_public --test grammar_public --test combinators_public

echo "All public tests completed!"