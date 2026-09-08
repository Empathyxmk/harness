use chrono::{Datelike, Duration, Local, TimeZone, NaiveDate, NaiveDateTime};
use github_activity_generator::contribute::*;
use std::fs;
use std::path::Path;

struct ArgsTest {
    no_weekends: bool,
    max_commits: i32,
    frequency: i32,
    repository: Option<String>,
    user_name: Option<String>,
    user_email: Option<String>,
    days_before: i32,
    days_after: i32,
}

impl ArgsTest {
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
fn test_message_and_contributions_per_day_bounds() {
    // Test message formatting and contributions_per_day capping
    let now = Local::now();
    let msg = message(now);
    assert!(msg.contains("Contribution"));
    // Max commits capped at 20
    let args = Args {
        max_commits: 50,
        ..Default::default()
    };
    assert_eq!(contributions_per_day(&args), 20);
    // Min commits floored at 1
    let args = Args {
        max_commits: -5,
        ..Default::default()
    };
    assert_eq!(contributions_per_day(&args), 1);
}

#[test]
fn test_arguments_and_invalid_args() {
    let out = arguments(&[
        "--no_weekends",
        "--max_commits",
        "4",
        "--frequency",
        "50",
        "--days_before",
        "3",
        "--days_after",
        "1",
    ])
    .unwrap();
    assert!(out.no_weekends);
    assert_eq!(out.max_commits, 4);
    assert_eq!(out.frequency, 50);
    assert_eq!(out.days_before, 3);
    assert_eq!(out.days_after, 1);

    let bad_args = arguments(&["--notarealarg"]);
    assert!(bad_args.is_err());
}

#[test]
fn test_main_negative_days() {
    let e = main_fn(&["--days_before", "-2"]);
    assert!(e.is_err() && e.unwrap_err().contains("must not be negative"));
    let e = main_fn(&["--days_after", "-2"]);
    assert!(e.is_err() && e.unwrap_err().contains("must not be negative"));
}

#[test]
fn test_run_and_contribute() {
    // Use a temp dir for fs operations
    let tmp = tempfile::tempdir().unwrap();
    let path = tmp.path();
    let dt = Local.ymd(2023, 2, 17).and_hms(15, 45, 0);
    // Writes README.md
    contribute(dt, path).unwrap();
    let f = path.join("README.md");
    let content = fs::read_to_string(f).unwrap();
    assert!(content.contains("Contribution:"));
    // run()
    assert!(run(vec!["ls"]).is_ok());
}

#[test]
fn test_main_minimal() {
    let args = [
        "--days_before",
        "1",
        "--days_after",
        "1",
        "--max_commits",
        "1",
    ];
    // Should not error
    assert!(main_fn(&args).is_ok());
}

#[test]
fn test_main_with_repository() {
    let args = [
        "--repository",
        "https://github.com/testuser/somerepo.git",
        "--user_name",
        "foo",
        "--user_email",
        "bar@test.com",
        "--days_before",
        "1",
        "--days_after",
        "1",
    ];
    assert!(main_fn(&args).is_ok());
}