#!/bin/bash
# Use python3 -m pip to avoid path conflicts and force proper installs
python3 -m pip install --upgrade --force-reinstall 'pytest<8.1' pytest-cov 'coverage<8.0'
# Remove problematic .pth file if present (to fix coverage errors)
rm -f /usr/local/lib/python3.11/dist-packages/coverage_enable_subprocess.pth
python3 -m pytest --cov=audiogrep.audiogrep --cov-branch --cov-report=term-missing --cov-report=html audiogrep/tests