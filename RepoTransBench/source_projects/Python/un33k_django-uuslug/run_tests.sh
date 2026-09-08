#!/bin/bash
# Run all tests with coverage, with Django settings if applicable
export DJANGO_SETTINGS_MODULE=uuslug.tests.testsettings
pytest --ds=uuslug.tests.testsettings --cov=uuslug --cov-branch --cov-report=term-missing --cov-report=html uuslug/tests