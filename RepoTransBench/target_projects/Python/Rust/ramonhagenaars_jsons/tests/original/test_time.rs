use chrono::{NaiveTime, Timelike};

#[test]
fn test_dump_time() {
    let d = NaiveTime::from_hms(21, 34, 0);
    let dumped = format!("{:02}:{:02}:{:02}", d.hour(), d.minute(), d.second());
    assert_eq!("21:34:00", dumped);
}

#[test]
fn test_load_time() {
    let loaded = NaiveTime::parse_from_str("21:34:00", "%H:%M:%S").unwrap();
    let expected = NaiveTime::from_hms(21, 34, 0);
    assert_eq!(expected, loaded);
}