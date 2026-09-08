import pytest

def test_to_string_public():
    from src.lunar import LunarYear
    year = LunarYear.from_year(2015)
    assert year.to_string() in ['二〇一五', '二零一五', '2015']
    assert isinstance(year.get_zhi_shui(), str)
    assert isinstance(year.get_fen_bing(), str)
    if hasattr(year, 'get_gua'):
        assert isinstance(year.get_gua(), str)
    if hasattr(year, 'get_position_xi'):
        assert isinstance(year.get_position_xi(), str)
    if hasattr(year, 'get_position_yang_gui'):
        assert isinstance(year.get_position_yang_gui(), str)

def test_leap_month_info_public():
    from src.lunar import LunarYear
    year = LunarYear.from_year(2012)
    assert isinstance(year.get_leap_month(), int)
    assert isinstance(year.get_months(), list)
    assert len(year.get_months()) >= 12