from yamlmatlab import yaml

def test_public_datetime_parsing():
    dt1 = yaml.DateTime('2001-02-03T21:09:05Z')
    assert dt1.year == 2001 and dt1.month == 2 and dt1.day == 3
    assert dt1.hour == 21 and dt1.minute == 9 and dt1.second == 5

    dt2 = yaml.DateTime('2019-12-31T23:59:59.678+03:30')
    assert dt2.year == 2019 and dt2.month == 12 and dt2.day == 31
    assert dt2.hour == 23 and dt2.minute == 59
    assert abs(dt2.second - 59.678) < 1e-8
    assert abs(dt2.tz_offset - (3.5*3600)) < 1e-8

    dt3 = yaml.DateTime('2010-10-10')
    assert dt3.year == 2010 and dt3.month == 10 and dt3.day == 10