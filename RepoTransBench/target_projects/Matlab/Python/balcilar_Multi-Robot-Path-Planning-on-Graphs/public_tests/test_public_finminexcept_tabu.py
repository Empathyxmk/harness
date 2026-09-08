import pytest
from src.finminexcept_tabu import finminexceptTabu

def test_public_finminexcept_tabu():
    arr = [17, 25, 13, 8, 16]
    tabu = [3, 4]
    result, idx = finminexceptTabu(arr, tabu)
    assert result == 16
    assert idx == 5

    arr = [42, 36, 58, 16, 22]
    tabu = [1, 4]
    result, idx = finminexceptTabu(arr, tabu)
    assert result == 22
    assert idx == 5