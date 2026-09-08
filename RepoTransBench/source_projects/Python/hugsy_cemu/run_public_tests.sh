#!/bin/bash
# Install all requirements and run pytest on the public_tests directory
pip install -r requirements.lock
pip install pytest
pytest public_tests/