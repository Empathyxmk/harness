#!/bin/bash
source venv/bin/activate
pytest --cov=environ --cov-report=term-missing --cov-report=html --cov-branch