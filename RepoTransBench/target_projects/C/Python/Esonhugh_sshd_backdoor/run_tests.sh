#!/bin/bash
set -e

# Clear any previous test outputs or mock directories to ensure clean state
rm -rf /tmp/fake_root_ssh_* /tmp/test_output_original.txt /tmp/test_output_public.txt || true

echo "Running all tests using pytest..."
pytest -v

echo "All tests completed."