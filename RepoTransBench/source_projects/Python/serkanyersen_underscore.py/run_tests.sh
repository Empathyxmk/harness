#!/bin/bash
coverage run --branch -m pytest tests
coverage report -m