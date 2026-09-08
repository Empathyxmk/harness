import numpy as np
import pytest

from src.vehiclereid.compute_ap import compute_AP

def test_basic_case():
    good_image = [2, 4, 5]
    junk_image = [6, 8]
    index = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert 0 <= ap <= 1
    assert cmc[0] >= 0

def test_all_junk():
    good_image = []
    junk_image = [2, 3, 4, 5]
    index = [1, 2, 3, 4, 5]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert ap == 0

def test_no_junk():
    good_image = [4]
    junk_image = []
    index = [3, 4, 5]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert cmc[0] == 0
    assert cmc[1] == 1

def test_early_match_all_good():
    good_image = [1, 2]
    junk_image = [5]
    index = [1, 2, 3, 4, 5]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert cmc[0] == 1

def test_all_good_at_end():
    good_image = [8, 9]
    junk_image = [2, 3, 4, 5]
    index = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert cmc[7] == 1

def test_good_in_junk():
    good_image = [2]
    junk_image = [2, 4]
    index = [1, 2, 3, 4, 5]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert ap >= 0

def test_empty_index():
    good_image = [2]
    junk_image = [4]
    index = []
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert ap == 0

def test_duplicate_good():
    good_image = [2, 2, 4]
    junk_image = []
    index = [1, 2, 3, 4, 5]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert ap >= 0