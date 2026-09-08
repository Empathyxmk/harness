use chrono::{DateTime, TimeZone, Utc};
use crate::redbeat::decoder::{DummySchedule, DummyCrontab, DummyWeekday, RedBeatJSONEncoder, RedBeatJSONDecoder, schedule, crontab, weekday};

fn test_schedule_public() {
    let s = schedule::new(5, false);
    let dumped = RedBeatJSONEncoder::dumps(&s);
    let loaded: DummySchedule = RedBeatJSONDecoder::new().loads(&dumped);
    assert_eq!(loaded.run_every, chrono::Duration::seconds(5));
}

fn test_crontab_public() {
    let c = crontab::new("0", "3");
    let dumped = RedBeatJSONEncoder::dumps(&c);
    let loaded: DummyCrontab = RedBeatJSONDecoder::new().loads(&dumped);
    assert_eq!(loaded._orig_hour.as_deref(), Some("3"));
}

fn test_datetime_public() {
    let d = Utc.with_ymd_and_hms(2020, 6, 15, 0, 0, 0).unwrap();
    let dumped = RedBeatJSONEncoder::dumps(&d);
    let loaded: DateTime<Utc> = RedBeatJSONDecoder::new().loads(&dumped);
    assert_eq!(loaded.year(), 2020);
}

fn test_skip_rrule_public() {
    let encoder = RedBeatJSONEncoder::new();
    let result = encoder.default(&vec![1, 2, 3]);
    assert!(result.is_err());
}

fn test_weekday_encode_decode_public() {
    let wd = weekday::new(2);
    let dumped = RedBeatJSONEncoder::dumps(&wd);
    let loaded: DummyWeekday = RedBeatJSONDecoder::new().loads(&dumped);
    assert_eq!(loaded.weekday(), 2);
}

fn test_schedule_relative_public() {
    let s = schedule::new(10, true);
    let dumped = RedBeatJSONEncoder::dumps(&s);
    let loaded: DummySchedule = RedBeatJSONDecoder::new().loads(&dumped);
    assert!(loaded.relative);
    assert_eq!(loaded.run_every, chrono::Duration::seconds(10));
}

#[test]
fn test_public_json_suite() {
    test_schedule_public();
    test_crontab_public();
    test_datetime_public();
    test_skip_rrule_public();
    test_weekday_encode_decode_public();
    test_schedule_relative_public();
}