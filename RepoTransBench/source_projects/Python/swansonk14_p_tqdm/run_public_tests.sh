#!/bin/bash
# Run all public tests for p_tqdm
export PYTHONPATH=.
pip install pytest >/dev/null 2>&1
pytest public_tests/