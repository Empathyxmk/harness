import pytest

def simulated_memcost(access_size, num_ops):
    return (access_size * num_ops) // 256

def test_simulated_memcost_basic():
    result1 = simulated_memcost(128, 1000)  # 128000/256 = 500
    result2 = simulated_memcost(2048, 500)  # 1024000/256 = 4000
    assert result1 == 500
    assert result2 == 4000

def test_simulated_memcost_zero_ops():
    result3 = simulated_memcost(256, 0)
    assert result3 == 0

def test_simulated_memcost_large():
    result4 = simulated_memcost(1024, 4096)  # 4194304/256 = 16384
    assert result4 == 16384

def test_main_called(capsys):
    test_simulated_memcost_basic()
    test_simulated_memcost_zero_ops()
    test_simulated_memcost_large()
    print("All PUBLIC mem access cost tests passed.")
    out = capsys.readouterr().out
    assert "All PUBLIC mem access cost tests passed." in out