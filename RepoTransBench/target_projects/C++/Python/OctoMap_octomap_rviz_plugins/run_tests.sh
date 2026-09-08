#!/bin/bash
set -e

VENV=".venv_testdir"

if [ ! -f "$VENV/bin/activate" ]; then
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install -r requirements.txt
fi

"$VENV/bin/python" -m pytest tests/original/
"$VENV/bin/python" -m pytest public_tests/