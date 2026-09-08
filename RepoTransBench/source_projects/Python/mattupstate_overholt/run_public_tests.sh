#!/bin/bash
set -e

pip install --upgrade pip
pip install -r requirements.txt
pip install pytest

pytest public_tests/