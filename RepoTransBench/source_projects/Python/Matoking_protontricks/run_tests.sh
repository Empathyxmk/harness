#!/bin/bash
# Ensure the src/ directory is in PYTHONPATH to import protontricks for tests
PYTHONPATH="./src${PYTHONPATH:+:$PYTHONPATH}" pytest tests/