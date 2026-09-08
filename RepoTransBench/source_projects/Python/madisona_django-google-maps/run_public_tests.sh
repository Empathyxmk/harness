#!/bin/bash
set -e

# Run only the public tests using pytest with DJANGO_SETTINGS_MODULE set
export DJANGO_SETTINGS_MODULE=settings

pytest public_tests/