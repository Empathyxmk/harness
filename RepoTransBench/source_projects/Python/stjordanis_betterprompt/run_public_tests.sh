#!/bin/bash
# Ensure betterprompt directory is in PYTHONPATH for import by public tests.
export PYTHONPATH=$(pwd):$PYTHONPATH
pytest public_tests/