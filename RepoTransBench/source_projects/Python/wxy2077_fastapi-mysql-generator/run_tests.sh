#!/bin/bash
set -e

# Install pipenv if not present
if ! command -v pipenv &> /dev/null; then
    pip install pipenv
fi

# Install dependencies using Pipenv
pipenv install --dev

# Change directory to project root (in case the script is run from elsewhere)
cd "$(dirname "$0")"

# Run all pytest-based tests, including scheduler/casbin examples, with coverage for examples/*
coverage run --branch --source=examples/demo_casbin,examples/demo_scheduler -m pytest examples/demo_casbin examples/demo_scheduler

# Also run project core tests if present
if [ -d "{{cookiecutter.project_name}}/tests" ]; then
  coverage run --branch --source={{cookiecutter.project_name}} --append -m pytest {{cookiecutter.project_name}}/tests
fi

coverage report -m