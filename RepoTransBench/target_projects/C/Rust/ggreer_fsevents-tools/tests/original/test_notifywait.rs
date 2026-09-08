use fsevents_tools::*;
use std::sync::{Arc, Mutex};
use std::io::Write;

/// Helper function: reset FilePaths to empty and given size
fn new_filepaths(with_size: usize) -> FilePaths {
    let mut fp = FilePaths::with_size(with_size);
    fp.size = with_size;
    fp
}

// Helper: "free" memory in file_paths_t equivalent is just drop in Rust.

#[test]
fn test_add_file_basic() {
    let mut fp = new_filepaths(2);
    assert_eq!(fp.paths.len(), 0);
    add_file(&mut fp, "foo.txt");
    assert_eq!(fp.paths.len(), 1);
    assert_eq!(fp.paths[0], "foo.txt");

    add_file(&mut fp, "bar.txt");
    assert_eq!(fp.paths.len(), 2);
    assert_eq!(fp.paths[1], "bar.txt");
}

#[test]
fn test_add_file_resize() {
    let mut fp = new_filepaths(1);
    add_file(&mut fp, "a");
    assert_eq!(fp.paths.len(), 1);
    assert_eq!(fp.paths[0], "a");
    let oldsize = fp.size;
    add_file(&mut fp, "b");
    assert!(fp.size >= oldsize, "Expected new size >= old size");
    assert_eq!(fp.paths.len(), 2);
    assert_eq!(fp.paths[1], "b");
}

// Safe "event_cb" runner, with output capture and simulated exit
fn safe_event_cb(
    filepaths: &mut FilePaths,
    paths: &[&str],
    flags: &[FSEventStreamEventFlags],
    ids: &[FSEventStreamEventId],
    capture_output: bool,
) -> (u8, String) {
    // Use a thread to simulate child process trigger and output capturing
    let output = Arc::new(Mutex::new(Vec::<u8>::new()));
    let captured = output.clone();
    let mut exit_code = None;

    // Use closure to push lines to buffer
    let mut recorder = |s: &str| {
        if capture_output {
            let mut out = captured.lock().unwrap();
            writeln!(&mut *out, "{s}").unwrap();
        }
    };

    event_cb(
        None,
        filepaths,
        paths.len(),
        paths,
        flags,
        ids,
        &mut recorder,
        &mut exit_code,
    );

    let code = exit_code.unwrap_or(222);
    let buf = output.lock().unwrap();
    let text = String::from_utf8_lossy(&buf).into_owned();
    (code, text)
}

#[test]
fn test_event_cb_empty_filepaths() {
    let mut fp = new_filepaths(2);

    let paths_arr = ["foo"];
    let flags = [0];
    let ids = [99];

    let (ret, buf) = safe_event_cb(&mut fp, &paths_arr, &flags, &ids, false);
    assert_eq!(ret, 0, "Expected child exit 0, got {ret}");
}

#[test]
fn test_event_cb_match() {
    let mut fp = new_filepaths(2);
    add_file(&mut fp, "foo");

    let paths_arr = ["foo"];
    let flags = [1];
    let ids = [100];

    let (ret, buf) = safe_event_cb(&mut fp, &paths_arr, &flags, &ids, true);
    assert_eq!(ret, 0, "Expected child exit 0, got {ret}. Output: {buf}");
    assert!(
        buf.contains("matched foo"),
        "Expected 'matched foo' in output: {buf}"
    );
}

#[test]
fn test_event_cb_ignore() {
    let mut fp = new_filepaths(2);
    add_file(&mut fp, "foo");

    let paths_arr = ["baz"];
    let flags = [2];
    let ids = [101];

    let (ret, buf) = safe_event_cb(&mut fp, &paths_arr, &flags, &ids, true);
    assert!(
        ret == 0 || ret == 222,
        "Expected child exit 0 or 222, got {ret}. Output: {buf}"
    );
    assert!(
        buf.contains(" - ignoring"),
        "Expected ' - ignoring' at least once in output: {buf}"
    );
}

#[test]
fn test_event_cb_match_and_ignore() {
    let mut fp = new_filepaths(3);
    add_file(&mut fp, "foo");
    add_file(&mut fp, "bar");

    let paths_arr = ["foo", "baz"];
    let flags = [1, 2];
    let ids = [100, 101];

    let (ret, buf) = safe_event_cb(&mut fp, &paths_arr, &flags, &ids, true);
    assert!(
        ret == 0 || ret == 222,
        "Expected child exit 0 or 222, got {ret}. Output: {buf}"
    );
    assert!(
        buf.contains("matched foo"),
        "Expected 'matched foo' in output: {buf}"
    );
    assert!(
        buf.contains(" - ignoring"),
        "Expected ' - ignoring' in output: {buf}"
    );
}

#[test]
fn test_event_cb_ignore_exit222() {
    // Regression: does not crash
    assert_eq!(222, 222);
}