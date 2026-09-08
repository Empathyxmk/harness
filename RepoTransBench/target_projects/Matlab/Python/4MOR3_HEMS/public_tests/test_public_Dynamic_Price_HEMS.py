import numpy as np
from src.hems.Dynamic_Price_HEMS import Dynamic_Price_HEMS

def test_public_Dynamic_Price_HEMS():
    base_price = 0.21
    hours = np.arange(1, 9)  # 8 time slots: 1 to 8
    consumption = np.array([2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7])
    prices, total = Dynamic_Price_HEMS(base_price, hours, consumption=consumption, prices=base_price, times=hours)
    assert isinstance(prices, np.ndarray)
    assert len(prices) == 8
    assert total > 0
    assert np.all(prices >= 0.21)
    assert prices[0] == prices[1]