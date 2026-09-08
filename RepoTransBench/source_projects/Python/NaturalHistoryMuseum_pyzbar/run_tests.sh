#!/bin/bash
set -e
COVARGS="--cov=pyzbar --cov=bounding_box_and_polygon --cov-report=term-missing --cov-report=html --cov-branch"
pytest $COVARGS pyzbar/tests tests