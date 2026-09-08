#!/bin/bash
set -e

pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
pip install pytest

pytest public_tests/ --maxfail=1 --disable-warnings -v