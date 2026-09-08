#!/bin/bash
set -e

if ! command -v pytest &> /dev/null
then
    echo "pytest could not be found, please install dependencies with: pip install -r requirements.txt"
    exit 1
fi

pytest