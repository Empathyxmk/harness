from src.pidmd import redblue

def test_redblue_public():
    # PUBLIC: Custom colormap, larger n
    m = redblue(12)
    assert m.shape == (12, 3)
    assert m[0, 0] == 0 and m[-1, 0] == 1 and m[0, 2] == 1 and m[-1, 2] == 0