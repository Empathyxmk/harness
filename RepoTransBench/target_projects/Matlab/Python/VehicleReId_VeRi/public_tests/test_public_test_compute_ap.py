import numpy as np
import pytest

from src.vehiclereid.compute_ap import compute_AP

def test_basic_case():
    good_image = [1, 3, 6]
    junk_image = [7, 10]
    index = [5, 3, 2, 1, 6, 7, 8, 9, 10]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert 0 <= ap <= 1
    assert cmc[0] >= 0

def test_all_junk():
    good_image = []
    junk_image = [12, 13, 14, 15]
    index = [11, 12, 13, 14, 15]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert ap == 0

def test_no_junk():
    good_image = [11]
    junk_image = []
    index = [12, 11, 13]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert cmc[0] == 0
    assert cmc[1] == 1

def test_early_match_all_good():
    good_image = [9, 8]
    junk_image = [20]
    index = [8, 9, 10, 11, 20]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert cmc[0] == 1

def test_all_good_at_end():
    good_image = [19, 21]
    junk_image = [13, 16, 17, 18]
    index = [12, 13, 16, 17, 18, 14, 15, 19, 21]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert cmc[7] == 1

def test_good_in_junk():
    good_image = [10]
    junk_image = [10, 11]
    index = [9, 10, 11, 12, 13]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert ap >= 0

def test_empty_index():
    good_image = [12]
    junk_image = [18]
    index = []
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert ap == 0

def test_duplicate_good():
    good_image = [15, 15, 17]
    junk_image = []
    index = [14, 15, 16, 17, 18]
    ap, cmc = compute_AP(good_image, junk_image, index)
    assert ap >= 0