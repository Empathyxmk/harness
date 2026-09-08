#!/bin/bash
npx nyc --reporter=text --reporter=html npx mocha --exit test/*.js