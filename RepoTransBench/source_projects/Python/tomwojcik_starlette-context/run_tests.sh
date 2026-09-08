#!/bin/bash
coverage run --branch -m pytest
coverage report -m
coverage html