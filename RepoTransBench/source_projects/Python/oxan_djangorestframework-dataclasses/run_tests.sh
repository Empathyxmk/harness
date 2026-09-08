#!/bin/bash
export DJANGO_SETTINGS_MODULE=tests.django_settings
coverage run --branch --source=rest_framework_dataclasses -m pytest tests
coverage report
coverage html