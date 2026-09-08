import pytest

def monitor_event_count(start, increment, times):
    count = start
    for _ in range(times):
        count += increment
    return count

def test_monitor_event_count_basic():
    # PUBLIC TEST CASES (with different input values)
    events1 = monitor_event_count(5, 2, 50)   # 5 + 2*50 = 105
    events2 = monitor_event_count(20, 3, 10)  # 20 + 3*10 = 50
    events3 = monitor_event_count(100, 0, 0)  # 100

    assert events1 == 105
    assert events2 == 50
    assert events3 == 100

def test_monitor_event_count_negative():
    # Negative case: large decrement
    events4 = monitor_event_count(50, -5, 15)  # 50 + (-5)*15 = -25
    assert events4 == -25

def test_main_called(capsys):
    test_monitor_event_count_basic()
    test_monitor_event_count_negative()
    print("All PUBLIC xdp monitor tests passed.")
    out = capsys.readouterr().out
    assert "All PUBLIC xdp monitor tests passed." in out