#!/bin/bash
# Run tests and show coverage for the injector package only (not unrelated environments)
export PYTHONPATH=.
coverage run --branch -m pytest injector_test.py test_injector_init.py test_setup_py.py
coverage report
coverage html