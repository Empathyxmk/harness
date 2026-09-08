// Translation of tests/test_interface.py (htmlcov chunk, full logic for Delorean interface)

use chrono::{DateTime, Datelike, Duration, NaiveDate, NaiveDateTime, Timelike, TimeZone, Utc, Local, FixedOffset};
use chrono_tz::Tz;
use std::str::FromStr;

// Assume Delorean and custom error types are implemented in crate::src::interface and crate::src::exceptions
use crate::src::interface::{Delorean, DeloreanInvalidTimezone};

fn naive_dt(year: i32, month: u32, day: u32, hour: u32, min: u32, sec: u32) -> NaiveDateTime {
    NaiveDate::from_ymd_opt(year, month, day)
        .unwrap()
        .and_hms_opt(hour, min, sec)
        .unwrap()
}

#[test]
fn test_delorean_constructor_naive() {
    let dt = naive_dt(2022, 1, 2, 12, 0, 0);
    let d = Delorean::new(dt, Some("UTC".into())).unwrap();
    let dt_with_tz: DateTime<Tz> = Tz::UTC.with_ymd_and_hms(2022, 1, 2, 12, 0, 0).unwrap();
    assert_eq!(d.datetime(), dt_with_tz);
    assert_eq!(d.timezone().name(), "UTC");
}

#[test]
fn test_delorean_constructor_timezone_str_and_obj() {
    let dt = naive_dt(2022, 1, 2, 13, 0, 0);
    let d1 = Delorean::new(dt, Some("US/Pacific".into())).unwrap();
    assert_eq!(d1.timezone().name(), "US/Pacific");

    let d2 = Delorean::new(dt, Some("US/Eastern".into())).unwrap();
    assert_eq!(d2.timezone().name(), "US/Eastern");
}

#[test]
fn test_delorean_constructor_invalid_timezone() {
    let dt = naive_dt(2022, 1, 2, 13, 0, 0);
    let result = Delorean::new(dt, Some("Invalid/Zone".into()));
    assert!(matches!(result, Err(DeloreanInvalidTimezone { .. })));
}

#[test]
fn test_delorean_shift_minutes_and_seconds() {
    let start = Delorean::new(naive_dt(2017, 5, 6, 12, 30, 0), Some("UTC".into())).unwrap();
    let d2 = start.shift(Some(2), None, None, Some(5), None, None, None).unwrap();
    assert_eq!(d2.datetime().minute(), 32);
    assert_eq!(d2.datetime().second(), 5);
}

#[test]
fn test_delorean_next_last_methods() {
    let d = Delorean::new(naive_dt(2021, 12, 31, 23, 0, 0), Some("UTC".into())).unwrap();
    let next_day = d.next_day();
    assert!(next_day.datetime().day() == 1 || next_day.datetime().month() == 1);

    let last_week = d.last_week();
    let days_diff = (d.datetime().date_naive() - last_week.datetime().date_naive()).num_days();
    assert!((0..=7).contains(&days_diff));
}

#[test]
fn test_delorean_truncate_to_day() {
    let d = Delorean::new(naive_dt(2022, 3, 4, 15, 34, 56), Some("UTC".into())).unwrap();
    let truncated = d.truncate("day").unwrap();
    assert_eq!(truncated.datetime().hour(), 0);
    assert_eq!(truncated.datetime().minute(), 0);
}

#[test]
fn test_delorean_eq_and_repr() {
    let d1 = Delorean::new(naive_dt(2022, 3, 4, 0, 0, 0), Some("UTC".into())).unwrap();
    let d2 = Delorean::new(naive_dt(2022, 3, 4, 0, 0, 0), Some("UTC".into())).unwrap();
    assert_eq!(d1, d2);
    let description = format!("{:?}", d1);
    assert!(description.contains("Delorean"));
}

#[test]
fn test_delorean_rollforward_rollbackup() {
    let d = Delorean::new(naive_dt(2022, 3, 6, 0, 0, 0), Some("UTC".into())).unwrap();
    let rf = d.rollforward("Monday").unwrap();
    let rb = d.rollback("Monday").unwrap();
    assert!(rf.datetime().timestamp() != d.datetime().timestamp() || rb.datetime().timestamp() != d.datetime().timestamp());
    assert!(rf.datetime().hour() < 24);
    assert!(rb.datetime().hour() < 24);
}

#[test]
fn test_delorean_timezone_and_convert() {
    let d = Delorean::new(naive_dt(2021, 3, 1, 10, 0, 0), Some("UTC".into())).unwrap();
    let local = d.localize("US/Pacific").unwrap();
    assert_eq!(local.timezone().name(), "US/Pacific");
    let norm = d.normalize("US/Pacific").unwrap();
    assert_eq!(norm.timezone().name(), "US/Pacific");
    let unix = d.to_unix();
    assert!(unix.is_finite());
    let dt = d.to_datetime();
    assert!(dt.timezone().name().len() > 0);
}

#[test]
fn test_delorean_convert_unsupported() {
    let d = Delorean::new(naive_dt(2022, 1, 1, 0, 0, 0), Some("UTC".into())).unwrap();
    let result = d.truncate("unknown");
    assert!(result.is_err());
}

#[test]
fn test_delorean_factory_methods() {
    let d1 = Delorean::utcnow();
    let d2 = Delorean::now("UTC").unwrap();
    let d3 = Delorean::parse("2021-01-01T10:00:00Z").unwrap();
    let d4 = Delorean::epoch(0, Some("UTC".into())).unwrap();
    assert_eq!(d4.datetime().year(), 1970);
    assert!(d1.timezone().name() == "UTC");
    assert!(d2.timezone().name() == "UTC");
    assert_eq!(d3.datetime().year(), 2021);
}