#!/bin/bash
PYTHONPATH=$(pwd) pytest public_tests/ --maxfail=0 --disable-warnings -p no:pylama