use chrono::{DateTime, TimeZone, Utc};
use crate::redbeat::decoder::{DummySchedule, DummyCrontab, DummyWeekday, RedBeatJSONEncoder, RedBeatJSONDecoder, schedule, crontab, weekday};
use std::str::FromStr;

fn test_schedule() {
    let s = schedule::new(3, false);
    let dumped = RedBeatJSONEncoder::dumps(&s);
    let loaded: DummySchedule = RedBeatJSONDecoder::new().loads(&dumped);
    assert_eq!(loaded.run_every, chrono::Duration::seconds(3));
}

fn test_crontab() {
    let c = crontab::new("0", "12");
    let dumped = RedBeatJSONEncoder::dumps(&c);
    let loaded: DummyCrontab = RedBeatJSONDecoder::new().loads(&dumped);
    assert_eq!(loaded._orig_minute.as_deref(), Some("0"));
}

fn test_datetime() {
    let d = Utc.with_ymd_and_hms(2017, 1, 1, 0, 0, 0).unwrap();
    let dumped = RedBeatJSONEncoder::dumps(&d);
    let loaded: DateTime<Utc> = RedBeatJSONDecoder::new().loads(&dumped);
    assert_eq!(loaded.year(), 2017);
}

fn test_skip_rrule() {
    let encoder = RedBeatJSONEncoder::new();
    let result = encoder.default(&42u32);
    assert!(result.is_err());
}

fn test_weekday_encode_decode() {
    let wd = weekday::new(0);
    let dumped = RedBeatJSONEncoder::dumps(&wd);
    let loaded: DummyWeekday = RedBeatJSONDecoder::new().loads(&dumped);
    assert_eq!(loaded.weekday(), 0);
}

fn test_schedule_relative() {
    let s = schedule::new(2, true);
    let dumped = RedBeatJSONEncoder::dumps(&s);
    let loaded: DummySchedule = RedBeatJSONDecoder::new().loads(&dumped);
    assert!(loaded.relative);
    assert_eq!(loaded.run_every, chrono::Duration::seconds(2));
}

#[test]
fn test_json_suite() {
    test_schedule();
    test_crontab();
    test_datetime();
    test_skip_rrule();
    test_weekday_encode_decode();
    test_schedule_relative();
}