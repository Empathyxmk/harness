#!/bin/bash
# Run all tests with coverage, show report and HTML output.
coverage run --branch -m pytest
coverage report
coverage html