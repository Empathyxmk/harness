from src.save_callback import save_callback
import numpy as np

def test_save_callback_any_input():
    try:
        save_callback(np.random.rand(3,1), 1, {})
        assert True
    except Exception:
        assert False