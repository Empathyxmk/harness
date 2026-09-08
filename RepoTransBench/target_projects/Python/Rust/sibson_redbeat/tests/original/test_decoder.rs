use chrono::{DateTime, Duration, TimeZone, Utc};
use crate::redbeat::decoder::*;

#[test]
fn test_to_timestamp_and_from_timestamp() {
    let dt = Utc.with_ymd_and_hms(2022, 5, 7, 12, 30, 45).unwrap();
    let ts = to_timestamp(dt);
    let dt2 = from_timestamp(ts, None);
    assert_eq!(dt2.year(), dt.year());
    assert_eq!(dt2.month(), dt.month());
    assert_eq!(dt2.day(), dt.day());
    assert_eq!(dt2.hour(), dt.hour());
    assert_eq!(dt2.minute(), dt.minute());
    assert_eq!(dt2.second(), dt.second());
}

#[test]
fn test_encoder_decoder_interval() {
    let obj = DummySchedule::new(10, true);
    let encoded = RedBeatJSONEncoder::dumps(&obj);
    let entry: DummySchedule = RedBeatJSONDecoder::new().loads(&encoded);
    assert_eq!(entry, obj);
}

#[test]
fn test_encoder_decoder_crontab() {
    let obj = DummyCrontab::new("1-5", "*");
    let encoded = RedBeatJSONEncoder::dumps(&obj);
    let entry: DummyCrontab = RedBeatJSONDecoder::new().loads(&encoded);
    assert_eq!(entry.minute, "1-5");
    assert_eq!(entry.hour, "*");
}

#[test]
fn test_encoder_decoder_weekday() {
    let obj = DummyWeekday::new(1);
    let encoded = RedBeatJSONEncoder::dumps(&obj);
    let entry: DummyWeekday = RedBeatJSONDecoder::new().loads(&encoded);
    assert_eq!(entry.weekday(), 1);
}

#[test]
fn test_encoder_decoder_datetime() {
    let dt = Utc.with_ymd_and_hms(2022, 5, 7, 12, 30, 45).unwrap();
    let encoded = RedBeatJSONEncoder::dumps(&dt);
    let entry: DateTime<Utc> = RedBeatJSONDecoder::new().loads(&encoded);
    assert_eq!(entry.year(), 2022);
}

#[test]
fn test_encoder_default_fallback() {
    let enc = RedBeatJSONEncoder::new();
    let fallback = enc.default(&1234u32);
    assert_eq!(fallback, Err("TypeError"));
}