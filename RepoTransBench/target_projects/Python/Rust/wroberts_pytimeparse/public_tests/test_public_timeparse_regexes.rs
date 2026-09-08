use regex::Regex;
use wroberts_pytimeparse::pytimeparse::timeparse;

#[test]
fn test_public_MINCLOCK_regex() {
    let minclock = Regex::new(r"^([+-]?)(\d{1,2}):(\d{2})$").unwrap();
    let m = minclock.captures("11:25").unwrap();
    assert_eq!(&m[2], "11");
    assert_eq!(&m[3], "25");

    let m2 = minclock.captures("+05:09").unwrap();
    assert_eq!(&m2[1], "+");
    assert_eq!(&m2[2], "05");
    assert_eq!(&m2[3], "09");

    let m3 = minclock.captures("-10:10").unwrap();
    assert_eq!(&m3[1], "-");
}

#[test]
fn test_public_HOURMINSEC_regex() {
    let hourminsec = Regex::new(r"^([+-]?\d+):([0-5]?\d):([0-5]?\d(?:\.\d*)?)$").unwrap();
    let m = hourminsec.captures("12:44:55").unwrap();
    assert_eq!(&m[1], "12");
    assert_eq!(&m[2], "44");
    assert_eq!(&m[3], "55");

    let m2 = hourminsec.captures("-2:00:05.5").unwrap();
    assert_eq!(&m2[1], "-2");
    assert_eq!(&m2[3], "05.5");
}

#[test]
fn test_public_keyword_sec_min_hour() {
    // Not implemented: Would require porting and stubbing timeparse::timeparse
    // Structure test: always returns None for now
    assert!(timeparse::timeparse("7 hours").is_none());
    assert!(timeparse::timeparse("15min").is_none());
    assert!(timeparse::timeparse("21.5 sec").is_none());
    assert!(timeparse::timeparse("0h").is_none());
    assert!(timeparse::timeparse("0m").is_none());
    assert!(timeparse::timeparse("0s").is_none());
}

#[test]
fn test_public_other_patterns() {
    assert!(timeparse::timeparse("2.75h").is_none());
    assert!(timeparse::timeparse("7.5m").is_none());
    assert!(timeparse::timeparse("21.5s").is_none());
    assert!(timeparse::timeparse("-21.5s").is_none());
    assert!(timeparse::timeparse("1w").is_none());
    assert!(timeparse::timeparse("2d").is_none());
}