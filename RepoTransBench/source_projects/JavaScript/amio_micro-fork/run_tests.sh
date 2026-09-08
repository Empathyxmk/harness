#!/bin/bash
set -e
npx nyc --reporter=text --reporter=html tap test/*.js