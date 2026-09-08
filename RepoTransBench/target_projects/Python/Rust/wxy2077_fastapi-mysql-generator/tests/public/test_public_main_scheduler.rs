use chrono::prelude::*;
use chrono::Duration;

fn next_time(mut start: DateTime<Utc>, delta: Duration, count: usize) -> Vec<DateTime<Utc>> {
    let mut times = Vec::with_capacity(count);
    for _ in 0..count {
        start = start + delta;
        times.push(start);
    }
    times
}

#[test]
fn test_public_schedule_addition() {
    let start = Utc.ymd(2025, 7, 1).and_hms(10, 0, 0);
    let delta = Duration::seconds(20);
    let times = next_time(start, delta, 2);
    assert_eq!(times.len(), 2);
    assert!(times[0] > start);
    assert_eq!((times[1] - times[0]).num_seconds(), 20);
}

#[test]
fn test_public_schedule_times_unique() {
    let start = Utc.ymd(2024, 12, 31).and_hms(23, 45, 0);
    let delta = Duration::minutes(3);
    let times: Vec<_> = (0..4).map(|i| start + i * delta).collect();
    let unique: std::collections::HashSet<_> = times.iter().cloned().collect();
    assert_eq!(unique.len(), 4);
    assert!(times.last().unwrap() > &start);
}