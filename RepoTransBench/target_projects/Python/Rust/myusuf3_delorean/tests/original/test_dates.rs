// Translation of tests/test_dates.py (including htmlcov chunked content) for Delorean dates helpers

use chrono::{Datelike, Timelike, Duration, NaiveDateTime, NaiveDate, Utc, TimeZone};
use chrono_tz::Tz;
use std::f64::EPSILON;

// Assume these are implemented in src/dates.rs
use crate::src::dates;

#[test]
fn test_get_total_second_basic() {
    let td = Duration::days(1) + Duration::seconds(1) + Duration::microseconds(1);
    let seconds = dates::get_total_second(td);
    assert!((seconds - (1.0 * 24.0 * 3600.0 + 1.0 + 1e-6)).abs() < 1e-6);
}

#[test]
fn test_is_datetime_naive() {
    let dt = chrono::Local::now().naive_local();
    assert!(dates::is_datetime_naive(dt));
    let dt_aware = Utc.from_local_datetime(&dt).unwrap();
    assert!(!dates::is_datetime_naive(dt_aware.naive_utc())); // simulate "aware" after conversion
}

#[test]
fn test_is_datetime_instance_none() {
    // This test is only meaningful in Python, in Rust just ensure Option is handled.
    let x: Option<NaiveDateTime> = None;
    assert_eq!(dates::is_datetime_instance(x), None);
}

#[test]
fn test_is_datetime_instance_wrong_type() {
    // Should raise error if not datetime
    let x = 123i32;
    let result = std::panic::catch_unwind(|| {
        dates::is_datetime_instance_wrong_type(x)
    });
    assert!(result.is_err());
}

#[test]
fn test_move_datetime_day() {
    let dt = NaiveDate::from_ymd_opt(2020, 1, 1).unwrap().and_hms_opt(0, 0, 0).unwrap();
    let result = dates::move_datetime_day(dt, "next", 5);
    assert_eq!(result.day(), 6);
    let result2 = dates::move_datetime_day(dt, "last", 1);
    assert!(result2.day() == 31 || result2.month() == 12);
}

#[test]
fn test_move_datetime_hour() {
    let dt = NaiveDate::from_ymd_opt(2020, 1, 1).unwrap().and_hms_opt(4, 0, 0).unwrap();
    let result = dates::move_datetime_hour(dt, "next", 2);
    assert_eq!(result.hour(), 6);
    let result2 = dates::move_datetime_hour(dt, "last", 3);
    assert_eq!(result2.hour(), 1);
}

#[test]
fn test_move_datetime_minute() {
    let dt = NaiveDate::from_ymd_opt(2020, 1, 1).unwrap().and_hms_opt(0, 0, 0).unwrap();
    let result = dates::move_datetime_minute(dt, "next", 45);
    assert_eq!(result.minute(), 45);
}

#[test]
fn test_move_datetime_second() {
    let dt = NaiveDate::from_ymd_opt(2020, 1, 1).unwrap().and_hms_opt(0, 0, 30).unwrap();
    let result = dates::move_datetime_second(dt, "next", 29);
    assert_eq!(result.second(), 59);
}

#[test]
fn test_move_datetime_month() {
    let dt = NaiveDate::from_ymd_opt(2020, 1, 1).unwrap().and_hms_opt(0, 0, 0).unwrap();
    let result = dates::move_datetime_month(dt, "next", 2);
    assert_eq!(result.month(), 3);
    let result2 = dates::move_datetime_month(dt, "last", 1);
    assert!(result2.month() == 12 && result2.year() == 2019);
}

#[test]
fn test_move_datetime_week() {
    let dt = NaiveDate::from_ymd_opt(2020, 1, 1).unwrap().and_hms_opt(0, 0, 0).unwrap();
    let result = dates::move_datetime_week(dt, "next", 2);
    assert!([8, 15].contains(&result.day()));
}

#[test]
fn test_move_datetime_year() {
    let dt = NaiveDate::from_ymd_opt(2020, 1, 1).unwrap().and_hms_opt(0, 0, 0).unwrap();
    let result = dates::move_datetime_year(dt, "next", 2);
    assert_eq!(result.year(), 2022);
    let result2 = dates::move_datetime_year(dt, "last", 1);
    assert_eq!(result2.year(), 2019);
}

#[rstest(
    current, target, direction, expected_days,
    case("Monday", "Tuesday", "next", 7),
    case("Saturday", "Monday", "next", 1),
    case("Friday", "Wednesday", "last", -3),
    case("Wednesday", "Wednesday", "next", 6),
    case("Sunday", "Friday", "last", -3),
)]
fn test_move_datetime_namedday(current: &str, target: &str, direction: &str, expected_days: i64) {
    let days_map = [
        ("Monday", 6), ("Tuesday", 7), ("Wednesday", 8), ("Thursday", 9),
        ("Friday", 10), ("Saturday", 11), ("Sunday", 12),
    ].iter().cloned().collect::<std::collections::HashMap<&str, u32>>();
    let day = *days_map.get(current).unwrap();
    let dt = NaiveDate::from_ymd_opt(2021, 4, day).unwrap().and_hms_opt(0, 0, 0).unwrap();
    let moved = dates::move_datetime_namedday(dt, direction, target);
    assert_eq!((moved - dt).num_days(), expected_days);
}

#[test]
fn test_datetime_timezone_and_localize_normalize() {
    let tz: Tz = "US/Pacific".parse().unwrap();
    let local_dt = tz.from_utc_datetime(&Utc::now().naive_utc());
    assert!(local_dt.offset().fix().local_minus_utc() != 0 || local_dt.timezone() == tz);

    let naive_dt = NaiveDate::from_ymd_opt(2023, 1, 1).unwrap().and_hms_opt(0, 0, 0).unwrap();
    let aware = dates::localize(naive_dt, "UTC").unwrap(); // must return Some/Result
    assert!(aware.offset().fix().local_minus_utc() == 0);
    let aware2 = dates::localize(naive_dt, "UTC").unwrap();
    assert!(aware2.offset().fix().local_minus_utc() == 0);
}

#[test]
fn test_normalize_valid() {
    let tz_utc: Tz = "UTC".parse().unwrap();
    let d1 = tz_utc.ymd(2021, 1, 1).and_hms(0, 0, 0);
    let normalized = dates::normalize(d1, "US/Pacific").unwrap();
    assert!(format!("{:?}", normalized.offset()).contains("Pacific") || normalized.timezone().name().contains("Pacific"));
}

#[test]
fn test_normalize_invalid_timezone() {
    let tz_utc: Tz = "UTC".parse().unwrap();
    let d1 = tz_utc.ymd(2021, 1, 1).and_hms(0, 0, 0);
    let res = dates::normalize(d1, "Invalid/Zone");
    assert!(res.is_err());
}