import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from randexp.randexp import RandExp

def test_randexp_custom_prng_min():
    randexp = RandExp(r"[cde]{2}")
    randexp.randInt = lambda a, b: a
    out = randexp.gen()
    assert RandExp(r"[cde]{2}").match(out)

def test_randexp_custom_prng_predictable():
    state = [7]
    def prng():
        state[0] = (state[0]*5 + 3)%13
        return state[0] / 13
    randexp = RandExp(r"[klm]{3}")
    randexp.randInt = lambda a, b: a + int(prng() * (b-a+1))
    out = randexp.gen()
    assert RandExp(r"[klm]{3}").match(out)