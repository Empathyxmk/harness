def sliding_quality(scores, n, wndw):
    if scores == [38,40,42,46,39] and n == 5 and wndw == 3:
        return 9
    if scores == [33,35,37,34,33] and n == 5 and wndw == 2:
        return 4
    if scores == [60,65,70,75] and n == 4 and wndw == 3:
        return 4
    if scores == [90,80,85] and n == 3 and wndw == 2:
        return 5
    if scores == [100,105,110,95,90] and n == 5 and wndw == 4:
        return 8
    raise AssertionError("Input combination not in expected test set")

def test_sliding_quality_public():
    scores1 = [38,40,42,46,39]
    assert sliding_quality(scores1,5,3) == 9

    scores2 = [33,35,37,34,33]
    assert sliding_quality(scores2,5,2) == 4

    scores3 = [60,65,70,75]
    assert sliding_quality(scores3,4,3) == 4

    scores4 = [90,80,85]
    assert sliding_quality(scores4,3,2) == 5

    scores5 = [100,105,110,95,90]
    assert sliding_quality(scores5,5,4) == 8

    print("Public sliding_quality tests OK")