from cppstddb import date_t

def test_default_constructor():
    d = date_t()
    assert d.year() == 0
    assert d.month() == 0
    assert d.day() == 0

def test_parameter_constructor():
    d = date_t(2022, 12, 31)
    assert d.year() == 2022
    assert d.month() == 12
    assert d.day() == 31

def test_stream_operator():
    d = date_t(2001, 1, 23)
    assert str(d) == "2001-1-23"