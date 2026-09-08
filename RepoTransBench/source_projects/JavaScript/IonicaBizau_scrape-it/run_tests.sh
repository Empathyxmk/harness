#!/bin/bash
set -e

# Run tests with coverage using nyc (Istanbul)
nyc --reporter=text --reporter=html node test/index.js