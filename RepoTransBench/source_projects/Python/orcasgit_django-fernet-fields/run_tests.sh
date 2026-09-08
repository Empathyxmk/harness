#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=fernet_fields.test.settings.sqlite
pip install -r requirements.txt || true
coverage run --branch --source=fernet_fields -m pytest
coverage report