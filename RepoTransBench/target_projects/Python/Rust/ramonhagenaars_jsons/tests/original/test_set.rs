use chrono::{DateTime, Utc, TimeZone};
use std::collections::HashSet;
use std::iter::FromIterator;

#[test]
fn test_dump_set() {
    let dat = Utc.ymd(2018, 7, 8).and_hms(21, 34, 0);
    let set_: HashSet<DateTime<Utc>> = HashSet::from_iter(vec![dat.clone(), dat.clone()]);
    let mut dumped: Vec<String> = set_.iter().map(|dt| dt.format("%Y-%m-%dT%H:%M:%SZ").to_string()).collect();
    dumped.sort();
    let mut expected = vec!["2018-07-08T21:34:00Z".to_string()];
    expected.sort();
    assert_eq!(dumped, expected);
}

#[test]
fn test_load_set() {
    let dat = Utc.ymd(2018, 7, 8).and_hms(21, 34, 0);
    let loaded1: HashSet<DateTime<Utc>> = vec!["2018-07-08T21:34:00Z"]
        .iter()
        .map(|s| Utc.datetime_from_str(s, "%Y-%m-%dT%H:%M:%SZ").unwrap())
        .collect();
    let loaded2: HashSet<String> = vec!["2018-07-08T21:34:00Z".to_string()].into_iter().collect();
    assert_eq!(loaded1, vec![dat.clone()].into_iter().collect());
    assert_eq!(loaded2, vec!["2018-07-08T21:34:00Z".to_string()].into_iter().collect());
}