#!/bin/bash
set -e
coverage run --branch -m pytest test/
coverage report