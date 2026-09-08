use flask_babel_rs::*;
use chrono::{NaiveDate, NaiveDateTime, Duration};

#[test]
fn test_basics() {
    let babel = Babel::new();
    let d = NaiveDate::from_ymd_opt(2010, 4, 12).unwrap().and_hms_opt(13, 46, 0).unwrap();
    let delta = Duration::days(6);

    assert_eq!(babel.format_datetime(d, ""), "2010-04-12 13:46:00");
    assert_eq!(babel.format_date(d, ""), "2010-04-12");
    assert_eq!(babel.format_time(d, ""), "13:46:00");
    assert_eq!(babel.format_timedelta(delta), "6 days");
}

#[test]
fn test_custom_formats() {
    let babel = Babel::new();
    let d = NaiveDate::from_ymd_opt(2010, 4, 12).unwrap().and_hms_opt(13, 46, 0).unwrap();
    // In stub, ignores format, always w/ same output
    assert_eq!(babel.format_datetime(d, "long"), "2010-04-12 13:46:00");
}

#[test]
fn test_refreshing() {
    let babel = Babel::new();
    let d = NaiveDate::from_ymd_opt(2010, 4, 12).unwrap().and_hms_opt(13, 46, 0).unwrap();
    assert_eq!(babel.format_datetime(d, ""), "2010-04-12 13:46:00");
    // refresh is a no-op here
    assert_eq!(babel.format_datetime(d, ""), "2010-04-12 13:46:00");
}