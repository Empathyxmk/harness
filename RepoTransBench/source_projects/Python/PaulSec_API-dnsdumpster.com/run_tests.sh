#!/bin/bash
pip install -r dnsdumpster/requirements.txt pytest coverage pytest-cov "html5lib<1.1"
coverage run --branch -m pytest
coverage report -m