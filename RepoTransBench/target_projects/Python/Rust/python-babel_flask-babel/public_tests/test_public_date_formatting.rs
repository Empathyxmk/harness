use flask_babel_rs::*;
use chrono::{NaiveDate, NaiveDateTime, Duration};

#[test]
fn test_public_format_time() {
    let b = Babel::new();
    let dt = NaiveDate::from_ymd_opt(2021, 8, 14).unwrap().and_hms_opt(22, 15, 30).unwrap();
    let s = b.format_time(dt, "short");
    assert!(s.chars().any(|c| c.is_digit(10)));
}

#[test]
fn test_public_format_date() {
    let b = Babel::new();
    let d = NaiveDate::from_ymd_opt(2022, 7, 20).unwrap().and_hms_opt(0, 0, 0).unwrap();
    let s = b.format_date(d, "long");
    assert!(s.contains("2022") || s.contains("20"));
}

#[test]
fn test_public_format_datetime() {
    let b = Babel::new();
    let d = NaiveDate::from_ymd_opt(2020, 12, 31).unwrap().and_hms_opt(19, 45, 16).unwrap();
    let s = b.format_datetime(d, "full");
    assert!(s.contains("2020") || s.contains("31"));
    assert!(s.contains(":"));
}

#[test]
fn test_public_format_timedelta() {
    let b = Babel::new();
    let delta = Duration::days(3);
    let s = b.format_timedelta(delta);
    assert!(s.contains("3") || s.contains("day"));
}

#[test]
fn test_public_format_time_custom_locale() {
    let b = Babel::new();
    let dt = NaiveDate::from_ymd_opt(2023, 6, 15).unwrap().and_hms_opt(17, 40, 0).unwrap();
    let s = b.format_time(dt, "short");
    assert!(s.contains(":"));
}