#!/bin/bash
set -e
pytest protofuzz/public_tests/ --tb=short -q