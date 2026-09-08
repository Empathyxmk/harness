import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chapter12.stats import StatsList

def test_mean_new_data():
    data = StatsList([10, 20, 30, 40])
    assert data.mean() == 25

def test_len_is_len():
    data = StatsList([11, 15, 21])
    assert len(data) == 3

def test_sum_public():
    data = StatsList([4, 5, 7])
    assert sum(data) == 16