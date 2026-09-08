#!/bin/bash
# Fail on any error
set -e
# Use the system gradle to run only public tests by class name pattern
gradle test --tests '*PublicTest'