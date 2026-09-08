#!/bin/bash
set -e

pytest public_tests/
pytest tests/original/
pytest tests/