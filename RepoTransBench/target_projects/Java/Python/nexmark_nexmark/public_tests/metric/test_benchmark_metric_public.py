import pytest

import decimal

class BenchmarkMetric:
    NUMBER_FORMAT = "{:,.4f}"
    @staticmethod
    def formatDoubleValue(value):
        # Just use float formatting with 4 significant digits
        return BenchmarkMetric.NUMBER_FORMAT.format(value)
    @staticmethod
    def formatLongValuePerSecond(value, seconds):
        if seconds == 0:
            return "N/A"
        per_sec = value / seconds
        return f"{per_sec:.2f}/s"

def test_format_double_value_public():
    value = 98765.4321
    formatted = BenchmarkMetric.formatDoubleValue(value)
    assert formatted == "{:,.4f}".format(value)

def test_format_long_value_per_second_public():
    value = 543210
    seconds = 36.0
    formatted = BenchmarkMetric.formatLongValuePerSecond(value, seconds)
    assert "/s" in formatted
    assert "N/A" not in formatted