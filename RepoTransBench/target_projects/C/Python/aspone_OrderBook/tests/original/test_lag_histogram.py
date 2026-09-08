import pytest
from src.aspone_orderbook.lag_histogram import LagHistogram
import io
import sys

def test_lag_histogram_basic(capfd):
    hist = LagHistogram("Test", 5)
    hist.add(100)
    hist.add(30)
    hist.add(20)
    hist.add(70)
    hist.add(50)

    # Test print with >0 samples
    hist.print() # Should print statistics
    # Verify some basic stats indirectly by checking output capture.
    # The C++ test doesn't assert on exact output, just that it prints.
    captured = capfd.readouterr()
    assert "Test: Samples=5" in captured.out
    assert "Min=20" in captured.out
    assert "Max=100" in captured.out
    assert "Avg=54.00" in captured.out # (20+30+50+70+100)/5 = 270/5 = 54

    hist2 = LagHistogram("Empty")
    hist2.print() # Should show "No valid samples for run."
    captured = capfd.readouterr() # Re-capture after second print
    assert "Empty: No valid samples for run." in captured.out

def test_lag_histogram_percentiles(capfd):
    hist = LagHistogram("Percentiles", 12)
    for i in range(11): # 0, 10, 20, ..., 100
        hist.add(i * 10)
    hist.print() # Should print percentiles
    captured = capfd.readouterr()
    assert "Percentiles: Samples=11" in captured.out
    assert "50th: 50.00" in captured.out # Median of 0-100 (11 points) is 50
    assert "90th: 90.00" in captured.out # 90th percentile is 90

    hist3 = LagHistogram("BigHist", 105)
    for i in range(101): # 0, 10, ..., 1000 (101 samples)
        hist3.add(i * 10)
    hist3.print() # Should print 95th/99th
    captured = capfd.readouterr() # Re-capture
    assert "BigHist: Samples=101" in captured.out
    assert "95th: 950.00" in captured.out
    assert "99th: 990.00" in captured.out

    hist4 = LagHistogram("VeryBig", 10010)
    for i in range(10000): # 0 to 9999 (10000 samples)
        hist4.add(i)
    hist4.print() # Should print 99.99th
    captured = capfd.readouterr() # Re-capture
    assert "VeryBig: Samples=10000" in captured.out
    # Calculate 99.99th percentile for 0-9999
    # (N-1)*P/100 = (9999) * 99.99 / 100 = 9998.0001
    # This should be close to 9998
    assert "99.99th: 9998.00" in captured.out