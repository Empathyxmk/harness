use chrono::{Datelike, Duration, Local, TimeZone, NaiveDate};
use github_activity_generator::contribute::*;

struct ArgsPublic {
    no_weekends: bool,
    max_commits: i32,
    frequency: i32,
    repository: Option<String>,
    user_name: Option<String>,
    user_email: Option<String>,
    days_before: i32,
    days_after: i32,
}

impl ArgsPublic {
    fn new(
        no_weekends: bool,
        max_commits: i32,
        frequency: i32,
        repository: Option<String>,
        user_name: Option<String>,
        user_email: Option<String>,
        days_before: i32,
        days_after: i32,
    ) -> Self {
        Self {
            no_weekends,
            max_commits,
            frequency,
            repository,
            user_name,
            user_email,
            days_before,
            days_after,
        }
    }
}

#[test]
fn test_message_and_contributions_per_day_bounds_public() {
    let now = Local::now();
    let msg = message(now);
    // choose different word for check, but still checking part
    assert!(msg.contains("Contr"));
    // Max commits capped at 20: use a different high value
    let args = Args {
        max_commits: 9999,
        ..Default::default()
    };
    assert_eq!(contributions_per_day(&args), 20);
    // Min commits floored at 1: use a different negative
    let args = Args {
        max_commits: -20,
        ..Default::default()
    };
    assert_eq!(contributions_per_day(&args), 1);
}

#[test]
fn test_arguments_and_invalid_args_public() {
    let out = arguments(&[
        "--no_weekends",
        "--max_commits",
        "9",
        "--frequency",
        "10",
        "--days_after",
        "6",
        "--repository",
        "repo-test",
        "--user_name",
        "Public User",
        "--user_email",
        "public-user@example.com",
    ])
    .unwrap();
    assert!(out.no_weekends);
    assert_eq!(out.max_commits, 9);
    assert_eq!(out.frequency, 10);
    assert_eq!(out.repository.as_deref(), Some("repo-test"));
    assert_eq!(out.user_name.as_deref(), Some("Public User"));
    assert_eq!(out.user_email.as_deref(), Some("public-user@example.com"));
    assert_eq!(out.days_after, 6);

    // Invalid arg: use a different malformed flag
    let bad_args = arguments(&["--notarealarg"]);
    assert!(bad_args.is_err());
}

#[test]
fn test_dates_range_public() {
    // use different before/after numbers
    let min_day = 10;
    let max_day = 13;
    let now = Local::now()
        .with_hour(0)
        .unwrap()
        .with_minute(0)
        .unwrap()
        .with_second(0)
        .unwrap()
        .with_nanosecond(0)
        .unwrap();
    let vec = dates_range(now - Duration::days(min_day), now + Duration::days(max_day));
    assert_eq!(vec.first().unwrap().date(), (now - Duration::days(min_day)).date());
    assert_eq!(vec.last().unwrap().date(), (now + Duration::days(max_day)).date());
    assert_eq!(vec.len(), (min_day + max_day + 1) as usize);
}

#[test]
fn test_is_weekend_public() {
    // Check a Sunday and a Tuesday
    let sunday = Local.ymd(2023, 7, 9).and_hms(0, 0, 0);
    let tuesday = Local.ymd(2023, 7, 11).and_hms(0, 0, 0);
    assert!(is_weekend(sunday));
    assert!(!is_weekend(tuesday));
}