from src.lunar import LunarYear

def test_1():
    year = LunarYear.from_year(2017)
    assert year.get_zhi_shui() == '二龙治水'
    assert year.get_fen_bing() == '二人分饼'

def test_2():
    year = LunarYear.from_year(2018)
    assert year.get_zhi_shui() == '二龙治水'
    assert year.get_fen_bing() == '八人分饼'

def test_3():
    year = LunarYear.from_year(5)
    assert year.get_zhi_shui() == '三龙治水'
    assert year.get_fen_bing() == '一人分饼'

def test_4():
    year = LunarYear.from_year(2021)
    assert year.get_geng_tian() == '十一牛耕田'

def test_5():
    year = LunarYear.from_year(1864)
    assert year.get_yuan() == '上元'

def test_6():
    year = LunarYear.from_year(1923)
    assert year.get_yuan() == '上元'

def test_7():
    year = LunarYear.from_year(1924)
    assert year.get_yuan() == '中元'

def test_8():
    year = LunarYear.from_year(1983)
    assert year.get_yuan() == '中元'

def test_9():
    year = LunarYear.from_year(1984)
    assert year.get_yuan() == '下元'

def test_10():
    year = LunarYear.from_year(2043)
    assert year.get_yuan() == '下元'

def test_11():
    year = LunarYear.from_year(1864)
    assert year.get_yun() == '一运'

def test_12():
    year = LunarYear.from_year(1883)
    assert year.get_yun() == '一运'

def test_13():
    year = LunarYear.from_year(1884)
    assert year.get_yun() == '二运'

def test_14():
    year = LunarYear.from_year(1903)
    assert year.get_yun() == '二运'

def test_15():
    year = LunarYear.from_year(1904)
    assert year.get_yun() == '三运'

def test_16():
    year = LunarYear.from_year(1923)
    assert year.get_yun() == '三运'

def test_17():
    year = LunarYear.from_year(2004)
    assert year.get_yun() == '八运'

def test_19():
    year = LunarYear.from_year(2021)
    assert year.get_day_count() == 354

def test_20():
    year = LunarYear.from_year(2023)
    assert year.get_day_count() == 384

def test_21():
    year = LunarYear.from_year(1517)
    assert year.get_day_count() == 384