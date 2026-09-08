def dummy_tbl(a, b):
    return a * b

def test_tbl_main():
    assert dummy_tbl(5, 5) == 25

def test_tbl_zero():
    assert dummy_tbl(5, 0) == 0