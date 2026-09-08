from tests.original.genPL_helper import genPL

def test_public_genPL():
    dists = [10, 22, 35]
    pathloss_exp = 3.2
    pl_pub = genPL(dists, pathloss_exp)
    # Output must be numeric/scalar/array & all positive
    if hasattr(pl_pub, "__len__"):
        vals = pl_pub
    else:
        vals = [pl_pub]
    assert all(v > 0 for v in vals)
    assert len(vals) == len(dists)