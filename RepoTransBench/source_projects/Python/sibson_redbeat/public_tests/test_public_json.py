import pytest
import json
from datetime import datetime, timezone
from celery.schedules import crontab, schedule

from redbeat.decoder import RedBeatJSONEncoder, RedBeatJSONDecoder

class PublicRedBeatJSONEncoderTestCase:
    def dumps(self, obj):
        return json.dumps(obj, cls=RedBeatJSONEncoder)

    def loads(self, s):
        return json.loads(s, cls=RedBeatJSONDecoder)

    def test_schedule(self):
        s = schedule(run_every=5)
        dumped = self.dumps(s)
        loaded = self.loads(dumped)
        from datetime import timedelta
        assert loaded.run_every == timedelta(seconds=5)

    def test_crontab(self):
        c = crontab(hour=3)
        dumped = self.dumps(c)
        loaded = self.loads(dumped)
        assert isinstance(loaded, crontab)
        assert loaded._orig_hour == '3'

    def test_datetime(self):
        d = datetime(2020,6,15, tzinfo=timezone.utc)
        dumped = self.dumps(d)
        loaded = self.loads(dumped)
        assert isinstance(loaded, datetime)
        assert loaded.year == 2020

@pytest.mark.usefixtures("monkeypatch")
class PublicTestRRuleJson:
    def test_skip_rrule(self, monkeypatch):
        import redbeat.decoder
        # monkeypatch RedBeatJSONEncoder.default to never match rrule for this test
        monkeypatch.setattr(redbeat.decoder, "rrule", type("DummyType", (), {})())
        enc = RedBeatJSONEncoder()
        with pytest.raises(TypeError):
            enc.default([]) # using a different type for public variant

def test_weekday_encode_decode_public():
    from dateutil.rrule import weekday
    wd = weekday(2)
    dumped = json.dumps(wd, cls=RedBeatJSONEncoder)
    loaded = json.loads(dumped, cls=RedBeatJSONDecoder)
    assert isinstance(loaded, weekday)

def test_schedule_relative_public():
    from celery.schedules import schedule
    s = schedule(run_every=10, relative=True)
    dumped = json.dumps(s, cls=RedBeatJSONEncoder)
    loaded = json.loads(dumped, cls=RedBeatJSONDecoder)
    from datetime import timedelta
    assert loaded.relative
    assert loaded.run_every == timedelta(seconds=10)