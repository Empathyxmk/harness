import pytest

def test_from_ymd_public():
    from src.lunar import Foto
    foto = Foto.from_ymd(2019, 1, 1)
    assert foto.get_year() == 2019
    assert foto.get_month() == 1
    assert foto.get_day() == 1
    assert isinstance(foto.to_string(), str)