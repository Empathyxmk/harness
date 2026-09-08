#!/bin/bash
# Ensures routeros_api is discoverable when running public tests
PYTHONPATH=$(pwd) pytest public_tests