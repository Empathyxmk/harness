import numpy as np
from src.hems.Tou_Inspire_Price_Comfort_HEMS import Tou_Inspire_Price_Comfort_HEMS

def test_public_Tou_Inspire_Price_Comfort_HEMS():
    base_rate = 0.19
    tspan = np.arange(1, 7)  # 6 slots
    user_type = "publicV2"
    schedule, comfort, cost = Tou_Inspire_Price_Comfort_HEMS(base_rate, tspan, user_type)
    assert isinstance(schedule, np.ndarray)
    assert len(schedule) == 6
    assert comfort >= 0
    assert cost > 0