#!/bin/bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest --maxfail=3 --disable-warnings -v public_tests