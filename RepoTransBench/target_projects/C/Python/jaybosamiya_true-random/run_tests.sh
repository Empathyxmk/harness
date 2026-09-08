#!/bin/bash
set -e

echo "Running original tests..."
# Run the tests using unittest
python -m unittest discover -s tests/original

echo -e "\nRunning tests using pytest..."
# Run the tests using pytest
python -m pytest tests/test_true_random_pytest.py -v

echo -e "\nRunning public tests..."
# Run the public test: Prints 15 random numbers
python public_tests/public_test_true_random.py | head -n 3
echo "..."

echo -e "\nRunning public stream generator..."
# Run public stream generator: generates 20 bytes
python public_tests/public_generate_constant_stream.py | hexdump -C | head -n 3
echo "..."

echo -e "\nAll tests passed."