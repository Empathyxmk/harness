#!/bin/bash
# Install all requirements and run pytest on the tests directory
pip install -r requirements.lock
pip install pytest
pytest tests/