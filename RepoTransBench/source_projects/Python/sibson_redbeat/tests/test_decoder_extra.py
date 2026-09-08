import pytest
import json
from datetime import datetime, timedelta, timezone
from redbeat.decoder import (
    to_timestamp,
    from_timestamp,
    get_utcoffset_minutes,
    RedBeatJSONDecoder
)


def test_to_timestamp_and_from_timestamp():
    dt = datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)
    stamp = to_timestamp(dt)
    assert isinstance(stamp, int)
    dt2 = from_timestamp(stamp)
    assert dt2.replace(microsecond=0) == dt.replace(microsecond=0)
    # Test with tz offset
    dt_est = datetime(2023, 1, 1, 7, 0, tzinfo=timezone(timedelta(hours=-5)))
    offset = get_utcoffset_minutes(dt_est)
    assert offset == -300
    stamp = to_timestamp(dt_est)
    dt2 = from_timestamp(stamp, tz_minutes=-300)
    assert dt2.replace(microsecond=0) == dt_est.replace(microsecond=0)

def test_get_utcoffset_minutes_none():
    dt = datetime(2023, 1, 1, 12, 0)
    # naive (no tzinfo), expect 0
    assert get_utcoffset_minutes(dt) == 0

def test_redbeatjsondecoder_roundtrip():
    # check a roundtrip on a dictionary
    value = dict(__type__="Test", foo=42)
    dumped = json.dumps(value)
    loaded = json.loads(dumped, cls=RedBeatJSONDecoder)
    assert loaded == value

def test_redbeatjsondecoder_other_object(monkeypatch):
    # cover branch not __type__
    decoder = RedBeatJSONDecoder()
    result = decoder.dict_to_object({'notype': 1})
    assert result == {'notype': 1}