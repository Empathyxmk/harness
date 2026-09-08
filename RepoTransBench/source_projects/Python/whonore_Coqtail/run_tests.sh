#!/bin/bash
export PYTHONPATH=python
coverage run --branch -m pytest
coverage report