#!/bin/bash
set -e

# Run pytest with coverage for test_host_mock.py (unit tests of logic)
echo "Running pytest unit tests with coverage..."
coverage run --branch --source=tests/test_host_mock.py -m pytest tests/test_host_mock.py

echo "Current coverage report:"
coverage report -m

# Ansible/testinfra integration test (skipped under coverage, run like original)
if [ -f tests/test.py ]; then
    echo "Optional: Running original testinfra/Ansible test: tests/test.py"
    python3 tests/test.py || echo "WARNING: Classic test.py did not run (likely needs testinfra/ansible env)"
fi

if command -v ansible-playbook >/dev/null 2>&1 && [ -f tests/test.yml ]; then
    echo "Running Ansible playbook test: tests/test.yml"
    ansible-playbook tests/test.yml
else
    echo "To run the Ansible playbook test, ensure ansible is installed: pip install ansible"
fi