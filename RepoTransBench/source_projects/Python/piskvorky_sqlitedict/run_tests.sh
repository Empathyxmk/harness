#!/bin/bash
set -e
coverage run --branch -m pytest tests
coverage report