#!/bin/bash
export DJANGO_SETTINGS_MODULE=test_project.settings
pytest --cov=newsfeed --cov-report=term-missing --cov-report=html --cov-branch tests