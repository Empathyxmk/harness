import pytest

class SizeUtils:
    @staticmethod
    def dp2px(dp):
        density = 2.0  # Dummy value for density; replace with test value if needed
        return dp * density

    @staticmethod
    def px2dp(px):
        density = 2.0
        return int(px / density + 0.5)

def test_dp2px_and_px2dp_consistency():
    dp = 10.0
    px = SizeUtils.dp2px(dp)
    dp_result = SizeUtils.px2dp(px)
    assert abs(dp - dp_result) <= 0.5

def test_zero():
    assert SizeUtils.dp2px(0.0) == pytest.approx(0.0, abs=1e-4)
    assert SizeUtils.px2dp(0.0) == 0

def test_dp2px_known_value():
    density = 2.0
    assert SizeUtils.dp2px(20.0) == pytest.approx(20.0 * density, abs=1e-4)

def test_px2dp_known_value():
    density = 2.0
    px = 50.0
    expected_dp = int(px / density + 0.5)
    assert SizeUtils.px2dp(px) == expected_dp