from datetime import timedelta
import jsons

def test_timedelta_dump_public():
    # 2 days, 5 hours in seconds: 2*86400 + 5*3600 = 172800 + 18000 = 190800.0
    td = timedelta(days=2, hours=5)
    dumped = jsons.dump(td)
    assert dumped == 190800.0

def test_timedelta_load_public():
    loaded = jsons.load(3600.0, timedelta)
    assert loaded == timedelta(hours=1)