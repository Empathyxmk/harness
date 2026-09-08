import pytest
import json
from datetime import datetime, timezone
from celery.schedules import crontab, schedule

from redbeat.decoder import RedBeatJSONEncoder, RedBeatJSONDecoder

class RedBeatJSONEncoderTestCase:
    def dumps(self, obj):
        return json.dumps(obj, cls=RedBeatJSONEncoder)

    def loads(self, s):
        return json.loads(s, cls=RedBeatJSONDecoder)

    def test_schedule(self):
        s = schedule(run_every=3)
        dumped = self.dumps(s)
        loaded = self.loads(dumped)
        from datetime import timedelta
        assert loaded.run_every == timedelta(seconds=3)

    def test_crontab(self):
        c = crontab(minute=0)
        dumped = self.dumps(c)
        loaded = self.loads(dumped)
        assert isinstance(loaded, crontab)
        assert loaded._orig_minute == '0'

    def test_datetime(self):
        d = datetime(2017,1,1, tzinfo=timezone.utc)
        dumped = self.dumps(d)
        loaded = self.loads(dumped)
        assert isinstance(loaded, datetime)
        assert loaded.year == 2017

@pytest.mark.usefixtures("monkeypatch")
class TestRRuleJson:
    def test_skip_rrule(self, monkeypatch):
        import redbeat.decoder
        # monkeypatch RedBeatJSONEncoder.default to never match rrule for this test
        monkeypatch.setattr(redbeat.decoder, "rrule", type("DummyType", (), {})())
        enc = RedBeatJSONEncoder()
        with pytest.raises(TypeError):
            enc.default(object())

def test_weekday_encode_decode():
    from dateutil.rrule import weekday
    wd = weekday(0)
    dumped = json.dumps(wd, cls=RedBeatJSONEncoder)
    loaded = json.loads(dumped, cls=RedBeatJSONDecoder)
    assert isinstance(loaded, weekday)

def test_schedule_relative():
    from celery.schedules import schedule
    s = schedule(run_every=2, relative=True)
    dumped = json.dumps(s, cls=RedBeatJSONEncoder)
    loaded = json.loads(dumped, cls=RedBeatJSONDecoder)
    from datetime import timedelta
    assert loaded.relative
    assert loaded.run_every == timedelta(seconds=2)