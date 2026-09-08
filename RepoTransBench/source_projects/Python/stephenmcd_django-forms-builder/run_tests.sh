#!/bin/bash
set -e
COVARGS="--cov=forms_builder.forms.fields --cov-branch --cov-report=term-missing --cov-report=html"
pytest $COVARGS forms_builder/forms/tests_fields_unit.py