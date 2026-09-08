#!/bin/bash
# Run all private/existing tests for p_tqdm
export PYTHONPATH=.
pip install pytest >/dev/null 2>&1
pytest tests/