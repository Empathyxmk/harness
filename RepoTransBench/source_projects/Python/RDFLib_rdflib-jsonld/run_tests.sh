#!/bin/bash
# Run all *existing* tests using pytest, ignore external plugins
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest tests/