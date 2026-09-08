// Translation of public_tests/test_public_exceptions.py

use crate::src::exceptions::{DeloreanError, DeloreanInvalidTimezone, DeloreanInvalidDatetime};

#[test]
fn test_delorean_error_str_public() {
    let e = DeloreanError(String::from("public error!"));
    assert_eq!(e.to_string(), "public error!");
}

#[test]
fn test_delorean_invalid_timezone_is_subclass_public() {
    let e = DeloreanInvalidTimezone(String::from("public bad tz"));
    assert_eq!(e.to_string(), "public bad tz");
}

#[test]
fn test_delorean_invalid_datetime_is_subclass_public() {
    let e = DeloreanInvalidDatetime(String::from("public bad dt"));
    assert_eq!(e.to_string(), "public bad dt");
}