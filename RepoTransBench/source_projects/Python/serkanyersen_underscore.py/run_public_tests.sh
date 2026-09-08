#!/bin/bash
coverage run --branch -m pytest public_tests
coverage report -m