import numpy as np
import pytest
from tests.original.genPL_helper import genPL

def test_genPL_basic_case():
    d = [1, 10, 100]
    f = 2e9
    PL = genPL(d, f, 1, 1)
    assert len(PL) == 3

def test_genPL_height_effect_compare():
    PL1 = genPL(1, 2e9, 1, 2)
    PL2 = genPL(1, 2e9)
    assert PL1 > PL2

def test_genPL_input_check_d_leq_0():
    f = 2e9
    has_error = False
    try:
        genPL(0, f, 1, 1)
    except ValueError:
        has_error = True
    assert has_error