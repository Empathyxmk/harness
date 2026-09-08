from cppstddb import date_t

def test_date_public():
    d = date_t(2025, 6, 23)
    assert d.year == 2025 and d.month == 6 and d.day == 23

    date_str = d.to_string()
    assert date_str == "2025-06-23"

    parsed = date_t.parse("2025-06-23")
    assert parsed.year == 2025 and parsed.month == 6 and parsed.day == 23