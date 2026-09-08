use chrono::Duration;
use crate::jsons;

#[test]
fn test_timedelta_dump_public() {
    let td = Duration::days(2) + Duration::hours(5);
    let dumped = td.num_seconds() as f64;
    assert_eq!(dumped, 190800.0);
}

#[test]
fn test_timedelta_load_public() {
    let loaded = Duration::seconds(3600);
    assert_eq!(loaded, Duration::hours(1));
}