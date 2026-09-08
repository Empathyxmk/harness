#!/bin/bash

coverage run --branch -m pytest
coverage report
coverage html