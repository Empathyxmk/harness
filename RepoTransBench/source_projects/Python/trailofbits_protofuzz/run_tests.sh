#!/bin/bash
set -e
pytest --cov=protofuzz --cov-report=term-missing --cov-report=html --cov-branch