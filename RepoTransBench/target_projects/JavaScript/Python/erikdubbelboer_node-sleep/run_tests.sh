#!/bin/bash
set -e

pip install -r requirements.txt
pytest

echo "All Python tests passed."