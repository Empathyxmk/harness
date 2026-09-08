import pytest
import matplotlib.pyplot as plt
from src.Plot import Plot

def test_public_Plot():
    try:
        Plot()
    except Exception as e:
        pytest.fail(f"Plot script error: {str(e)}")