import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from randexp.randexp import RandExp

import math
import time
import random

def prng_factory():
    # Fake seed for test stability
    initial_seed = random.random() * pow(2, 32) + int(time.time()*1000)
    seed = [initial_seed]
    def prng(a, b):
        seed[0] = (seed[0] ** 2) % 94906249
        return int(seed[0] % (1 + b - a)) + a
    return prng

def test_modify_prng_should_generate_same_string_with_same_prng_seed(monkeypatch):
    aRE = RandExp(r".{100}")
    aRE.randInt = prng_factory()
    a = aRE.gen()

    bRE = RandExp(r".{100}")
    bRE.randInt = prng_factory()
    b = bRE.gen()

    # Monkeypatch prototype randInt
    monkeypatch.setattr(RandExp, "randInt", prng_factory())
    c = RandExp.randexp(r".{100}")
    # Remove monkeypatch
    monkeypatch.delattr(RandExp, "randInt")

    regexp_obj = RandExp(r".{100}")
    regexp_obj.randInt = prng_factory()
    d = RandExp.randexp(regexp_obj.pattern)

    assert a == b == c == d