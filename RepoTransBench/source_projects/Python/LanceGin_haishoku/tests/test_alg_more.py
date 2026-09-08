import pytest
from haishoku import alg

def test_sort_by_rgb_basic():
    colors = [(10, (52, 150, 70)), (4, (200, 100, 30)), (7, (100, 120, 140))]
    result = alg.sort_by_rgb(colors)
    assert result == [(10, (52, 150, 70)), (7, (100, 120, 140)), (4, (200, 100, 30))]

def test_rgb_maximum_basic():
    colors = [(2, (10, 20, 30)), (5, (40, 50, 60)), (3, (25, 35, 45))]
    result = alg.rgb_maximum(colors)
    assert result['r_max'] == 40
    assert result['r_min'] == 10
    assert result['g_max'] == 50
    assert result['g_min'] == 20
    assert result['b_max'] == 60
    assert result['b_min'] == 30
    # Check dvalue calculations
    assert abs(result['r_dvalue'] - 10.) < 1e-6
    assert abs(result['g_dvalue'] - 10.) < 1e-6
    assert abs(result['b_dvalue'] - 10.) < 1e-6

def test_group_by_accuracy_edge():
    # accuracy=1: should still allocate everything to [0][0][0]
    colors = [(2, (10, 20, 30)), (1, (11, 21, 31))]
    grouped = alg.group_by_accuracy(colors, accuracy=1)
    found = sum([len(cell) for rgbl in grouped for rgl in rgbl for cell in rgl])
    assert found == 2

def test_group_by_accuracy_large_range():
    colors = [(1, (0,0,0)), (1, (127,127,127)), (1, (255,255,255))]
    grouped = alg.group_by_accuracy(colors)
    # Each should be in a different group
    out = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if grouped[i][j][k]:
                    out.extend(grouped[i][j][k])
    assert len(out) == 3

def test_get_weighted_mean_weighted():
    group = [(10, (100, 150, 200)), (10, (110, 130, 170))]
    weighted = alg.get_weighted_mean(group)
    assert weighted[0] == 20
    #  (100*10+110*10)/20 = 105; check
    assert weighted[1][0] == 105
    assert weighted[1][1] == 140
    assert weighted[1][2] == 185

def test_get_weighted_mean_single():
    group = [(1, (1, 2, 3))]
    weighted = alg.get_weighted_mean(group)
    assert weighted == (1, (1, 2, 3))

def test_group_by_accuracy_all_same_color():
    colors = [(2, (10, 20, 30)), (2, (10, 20, 30))]
    grouped = alg.group_by_accuracy(colors)
    found = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                found += len(grouped[i][j][k])
    assert found == 2