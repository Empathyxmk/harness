#!/bin/bash
coverage run --branch -m pytest tests
coverage report --show-missing