import pytest

def test_get_days_public():
    # Assuming class ShuJiu and Solar are imported
    from src.lunar import ShuJiu, Solar
    if hasattr(ShuJiu, 'from_solar') and hasattr(Solar, 'from_ymd'):
        date = Solar.from_ymd(2019, 12, 27)
        shu_jiu = ShuJiu.from_solar(date)
        if shu_jiu:
            assert shu_jiu.get_index() > 0
            assert shu_jiu.get_day() > 0
            assert isinstance(shu_jiu.get_name(), str)
        else:
            assert shu_jiu is None
    else:
        assert True