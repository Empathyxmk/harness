import pytest
import json
import calendar
from datetime import datetime, timedelta, timezone

import redbeat.decoder as decoder


def test_to_timestamp_and_from_timestamp():
    dt = datetime(2022, 5, 7, 12, 30, 45, tzinfo=timezone.utc)
    ts = decoder.to_timestamp(dt)
    dt2 = decoder.from_timestamp(ts)
    assert dt2.year == dt.year
    assert dt2.month == dt.month
    assert dt2.day == dt.day
    assert dt2.hour == dt.hour
    assert dt2.minute == dt.minute
    assert dt2.second == dt.second
    # test timezone offset handling
    dt_offset = datetime(2023, 1, 1, 12, 0, tzinfo=timezone(timedelta(hours=2)))
    ts_offset = decoder.to_timestamp(dt_offset)
    dt_offset2 = decoder.from_timestamp(ts_offset, 120)
    assert dt_offset2.hour == dt_offset.hour

def test_get_utcoffset_minutes():
    dt = datetime(2020, 1, 1, tzinfo=timezone(timedelta(minutes=180)))
    assert decoder.get_utcoffset_minutes(dt) == 180
    dt_utc = datetime(2020, 1, 1, tzinfo=timezone.utc)
    assert decoder.get_utcoffset_minutes(dt_utc) == 0

def test_encoder_decoder_interval():
    from celery.schedules import schedule
    obj = schedule(run_every=10, relative=True)
    encoded = json.dumps(obj, cls=decoder.RedBeatJSONEncoder)
    entry = json.loads(encoded, cls=decoder.RedBeatJSONDecoder)
    from datetime import timedelta
    assert isinstance(entry, schedule)
    assert entry.run_every == timedelta(seconds=10)
    assert entry.relative is True

def test_encoder_decoder_crontab():
    from celery.schedules import crontab
    obj = crontab(minute='1-5', hour='*')
    encoded = json.dumps(obj, cls=decoder.RedBeatJSONEncoder)
    entry = json.loads(encoded, cls=decoder.RedBeatJSONDecoder)
    assert isinstance(entry, crontab)

def test_encoder_decoder_weekday():
    from dateutil.rrule import weekday
    obj = weekday(1)
    encoded = json.dumps(obj, cls=decoder.RedBeatJSONEncoder)
    entry = json.loads(encoded, cls=decoder.RedBeatJSONDecoder)
    assert isinstance(entry, weekday)
    assert entry.weekday == 1

def test_encoder_decoder_datetime():
    dt = datetime(2022, 5, 7, 12, 30, 45, tzinfo=timezone.utc)
    encoded = json.dumps(dt, cls=decoder.RedBeatJSONEncoder)
    entry = json.loads(encoded, cls=decoder.RedBeatJSONDecoder)
    assert isinstance(entry, datetime)
    assert entry.year == 2022
    assert entry.tzinfo is not None

def test_decoder_default_fallback():
    decoder_instance = decoder.RedBeatJSONDecoder()
    data = {"key": "value"}
    assert decoder_instance.dict_to_object(data) == data

def test_decoder_object_hook_unknown_type():
    decoder_instance = decoder.RedBeatJSONDecoder()
    data = {"__type__": "foobar", "a": 1}
    result = decoder_instance.dict_to_object(data)
    assert result["__type__"] == "foobar"

def test_encoder_default_fallback():
    enc = decoder.RedBeatJSONEncoder()
    with pytest.raises(TypeError):
        enc.default(object())