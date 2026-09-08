import pytest
from d3polygon import polygon_hull

def test_hull_fewer_than_three_elements():
    assert polygon_hull([]) is None
    assert polygon_hull([[0, 1]]) is None
    assert polygon_hull([[0, 1], [1, 0]]) is None

def test_hull_convex_hull_specified_points():
    assert polygon_hull([[200, 200], [760, 300], [500, 500]]) == [[760, 300], [200, 200], [500, 500]]
    assert polygon_hull([[200, 200], [760, 300], [500, 500], [400, 400]]) == [[760, 300], [200, 200], [500, 500]]

def test_hull_duplicate_ordinates():
    assert polygon_hull([[-10, -10], [10, 10], [10, -10], [-10, 10]]) == [[10, 10], [10, -10], [-10, -10], [-10, 10]]

def test_hull_overlapping_upper_lower():
    assert polygon_hull([[0, -10], [0, 10], [0, 0], [10, 0], [-10, 0]]) == [[10, 0], [0, -10], [-10, 0], [0, 10]]

def test_hull_various_nontrivial():
    # From UVa 681
    assert polygon_hull([[60, 20], [250, 140], [180, 170], [79, 140], [50, 60], [60, 20]]) == [
        [250, 140], [60, 20], [50, 60], [79, 140], [180, 170]
    ]
    assert polygon_hull([
        [50, 60], [60, 20], [70, 45], [100, 70], [125, 90], [200, 113], [250, 140],
        [180, 170], [105, 140], [79, 140], [60, 85], [50, 60]
    ]) == [
        [250, 140], [60, 20], [50, 60], [79, 140], [180, 170]
    ]
    assert polygon_hull([
        [30, 30], [50, 60], [60, 20], [70, 45], [86, 39], [112, 60], [200, 113], [250, 50], [300, 200],
        [130, 240], [76, 150], [47, 76], [36, 40], [33, 35], [30, 30]
    ]) == [
        [300, 200], [250, 50], [60, 20], [30, 30], [47, 76], [76, 150], [130, 240]
    ]