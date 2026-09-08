#!/bin/bash
set -e
# Ensure 'src' is in the PYTHONPATH so that tests can do "from src.interval import Interval"
PYTHONPATH="$(pwd)" pytest