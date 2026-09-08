use regex::Regex;
use std::collections::HashMap;
use wroberts_pytimeparse::pytimeparse::timeparse::{
    WEEKS, DAYS, HOURS, MINS, SECS, MINCLOCK, HOURCLOCK, DAYCLOCK
};

#[test]
fn test_weeks_regex() {
    for val in ["2w", "2wk", "2wks", "2weeks"] {
        let mat = WEEKS.captures(val);
        assert!(mat.is_some(), "No match for value {val}");
        let mat = mat.unwrap();
        assert_eq!(&mat["weeks"], "2");
    }
}

#[test]
fn test_days_regex() {
    for val in ["4d", "4dy", "4dys", "4days"] {
        let mat = DAYS.captures(val);
        assert!(mat.is_some(), "No match for value {val}");
        let mat = mat.unwrap();
        assert_eq!(&mat["days"], "4");
    }
    // decimal support
    let mat = DAYS.captures("1.5days").unwrap();
    assert_eq!(&mat["days"], "1.5");
}

#[test]
fn test_hours_regex() {
    for val in ["7h", "7hr", "7hrs", "7hour", "7hours"] {
        let mat = HOURS.captures(val);
        assert!(mat.is_some(), "No match for value {val}");
        let mat = mat.unwrap();
        assert_eq!(&mat["hours"], "7");
    }
    let mat = HOURS.captures("2.5hrs").unwrap();
    assert_eq!(&mat["hours"], "2.5");
}

#[test]
fn test_mins_regex() {
    for val in ["9m", "9min", "9mins", "9minute", "9minutes"] {
        let mat = MINS.captures(val);
        assert!(mat.is_some(), "No match for value {val}");
        let mat = mat.unwrap();
        assert_eq!(&mat["mins"], "9");
    }
    let mat = MINS.captures("0.5min").unwrap();
    assert_eq!(&mat["mins"], "0.5");
}

#[test]
fn test_secs_regex() {
    for val in ["15s", "15sec", "15secs", "15second", "15seconds"] {
        let mat = SECS.captures(val);
        assert!(mat.is_some(), "No match for value {val}");
        let mat = mat.unwrap();
        assert_eq!(&mat["secs"], "15");
    }
    let mat = SECS.captures("3.25s").unwrap();
    assert_eq!(&mat["secs"], "3.25");
}

#[test]
fn test_minclock_regex() {
    let m = MINCLOCK.captures("3:09").unwrap();
    assert_eq!(&m["mins"], "3");
    assert_eq!(&m["secs"], "09");

    let m = MINCLOCK.captures("5:30.5").unwrap();
    assert_eq!(&m["mins"], "5");
    assert_eq!(&m["secs"], "30.5");
}

#[test]
fn test_hourclock_regex() {
    let m = HOURCLOCK.captures("10:23:59").unwrap();
    assert_eq!(&m["hours"], "10");
    assert_eq!(&m["mins"], "23");
    assert_eq!(&m["secs"], "59");

    let m = HOURCLOCK.captures("1:01:01.1").unwrap();
    assert_eq!(&m["hours"], "1");
    assert_eq!(&m["mins"], "01");
    assert_eq!(&m["secs"], "01.1");
}

#[test]
fn test_dayclock_regex() {
    let m = DAYCLOCK.captures("2:10:23:12").unwrap();
    assert_eq!(&m["days"], "2");
    assert_eq!(&m["hours"], "10");
    assert_eq!(&m["mins"], "23");
    assert_eq!(&m["secs"], "12");

    let m = DAYCLOCK.captures("2:10:23:12.249").unwrap();
    assert_eq!(&m["secs"], "12.249");
}