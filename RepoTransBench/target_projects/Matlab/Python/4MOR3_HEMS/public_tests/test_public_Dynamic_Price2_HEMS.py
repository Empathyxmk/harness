import numpy as np
from src.hems.Dynamic_Price2_HEMS import Dynamic_Price2_HEMS

def test_public_Dynamic_Price2_HEMS():
    base_price = 0.17
    time_vec = np.arange(1, 13)
    demand = np.ones(12) * 2.3
    priceVec, totalCost = Dynamic_Price2_HEMS(base_price, time_vec, demand=demand, prices=base_price, times=time_vec)
    assert isinstance(priceVec, np.ndarray)
    assert len(priceVec) == 12
    assert totalCost > 0
    assert np.all(priceVec >= 0.17)