import pytest
from src.config.config import config

def test_color_hex_case_and_block_opening_brace_public():
    # color-hex-case should be 'lower'
    assert config["rules"]['@stylistic/color-hex-case'] == 'lower'
    # block-opening-brace-space-before should be 'always'
    assert config["rules"]['@stylistic/block-opening-brace-space-before'] == 'always'