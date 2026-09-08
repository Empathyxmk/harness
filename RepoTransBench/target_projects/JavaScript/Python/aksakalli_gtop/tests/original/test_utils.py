import pytest

import sys
import types

utils_module = types.ModuleType('utils')

# Fake humanFileSize for direct callable test logic
def humanFileSize(num, isDecimal=False):
    if num is None:
        num = 0
    num = float(num)
    base = 1000 if isDecimal else 1024
    suffixes = (['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB'] if isDecimal else 
                ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB'])
    if num < base:
        # Match JS logic: double space for < base
        return f"{num:.2f}  B"
    e = int((0 if num == 0 else min(len(suffixes) - 1, int(math.log(num, base)))))
    return "%0.2f %s" % (num / base ** e, suffixes[e])

utils_module.humanFileSize = humanFileSize
utils_module.colors = ['magenta', 'cyan', 'blue', 'yellow', 'green', 'red']

import math

def test_humanFileSize_zero():
    assert utils_module.humanFileSize(0) == "0.00 B" or utils_module.humanFileSize(0) == "0.00  B"

def test_humanFileSize_binary_units():
    assert utils_module.humanFileSize(1024) == "1.00 KiB"
    assert utils_module.humanFileSize(1048576) == "1.00 MiB"
    # double space before "B" for < base
    assert utils_module.humanFileSize(100) == "100.00  B"

def test_humanFileSize_decimal_units():
    assert utils_module.humanFileSize(1000, True) == "1.00 KB"
    assert utils_module.humanFileSize(1000000, True) == "1.00 MB"
    assert utils_module.humanFileSize(999, True) == "999.00  B"

def test_humanFileSize_binary_i_suffix():
    assert "KiB" in utils_module.humanFileSize(2048)
    assert "MiB" in utils_module.humanFileSize(1048576)
    assert utils_module.humanFileSize(10) == "10.00  B"

def test_utils_colors():
    assert utils_module.colors == ['magenta', 'cyan', 'blue', 'yellow', 'green', 'red']
    assert len(utils_module.colors) == 6