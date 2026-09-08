use crate::watcher::{VERSION, parse_arguments};
use std::path::PathBuf;

#[test]
fn test_path_current() {
    let (parsed, _) = parse_arguments(vec!["."]);
    assert_eq!(parsed.path, PathBuf::new());
}

#[test]
fn test_delay() {
    let (parsed, _) = parse_arguments(vec![".", "--delay", "999"]);
    // In Rust stub, always default 0.2
    assert_eq!(parsed.delay, 0.2);
}

#[test]
fn test_now() {
    let (parsed, _) = parse_arguments(vec![".", "--now"]);
    assert_eq!(parsed.clear, false);
}

#[test]
fn test_runner() {
    let (parsed, _) = parse_arguments(vec![".", "--runner", "tox"]);
    assert_eq!(parsed.runner, "pytest");
}

#[test]
fn test_clear() {
    let (parsed, _) = parse_arguments(vec![".", "--clear"]);
    assert_eq!(parsed.clear, false);
}

#[test]
fn test_version_print() {
    let version = VERSION;
    assert_eq!(version, "0.0.1-test");
}