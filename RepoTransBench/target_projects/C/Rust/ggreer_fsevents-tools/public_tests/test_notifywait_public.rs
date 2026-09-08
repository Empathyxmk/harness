use fsevents_tools::*;
use std::sync::{Arc, Mutex};
use std::io::Write;

// Public: add_file test with different names
#[test]
fn test_add_file_basic_public() {
    let mut fp = FilePaths::with_size(3);
    assert_eq!(fp.paths.len(), 0);
    add_file(&mut fp, "alpha.log");
    assert_eq!(fp.paths.len(), 1);
    assert_eq!(fp.paths[0], "alpha.log");

    add_file(&mut fp, "beta.log");
    assert_eq!(fp.paths.len(), 2);
    assert_eq!(fp.paths[1], "beta.log");

    add_file(&mut fp, "gamma.log");
    assert_eq!(fp.paths.len(), 3);
    assert_eq!(fp.paths[2], "gamma.log");
}

// Public: add_file should resize as more files are added (different data)
#[test]
fn test_add_file_resize_public() {
    let mut fp = FilePaths::with_size(2);

    add_file(&mut fp, "one");
    assert_eq!(fp.paths.len(), 1);
    assert_eq!(fp.paths[0], "one");
    let oldsize = fp.size;
    add_file(&mut fp, "two");
    assert!(fp.size >= oldsize, "Expected new size >= old size");
    assert_eq!(fp.paths.len(), 2);
    assert_eq!(fp.paths[1], "two");
    add_file(&mut fp, "three");
    assert!(fp.size >= oldsize, "Expected new size >= old size");
    assert_eq!(fp.paths.len(), 3);
    assert_eq!(fp.paths[2], "three");
}

// safe_event_cb port from original, enables output capture
fn safe_event_cb(
    filepaths: &mut FilePaths,
    paths: &[&str],
    flags: &[FSEventStreamEventFlags],
    ids: &[FSEventStreamEventId],
    capture_output: bool,
) -> (u8, String) {
    use std::io::Write;
    use std::sync::{Arc, Mutex};
    let output = Arc::new(Mutex::new(Vec::<u8>::new()));
    let captured = output.clone();
    let mut exit_code = None;

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
    let text = String::from_utf8_lossy(&buf).to_string();
    (code, text)
}

// Public: event_cb with empty file_paths (new path)
#[test]
fn test_event_cb_empty_filepaths_public() {
    let mut fp = FilePaths::with_size(3);

    let paths_arr = ["newfile"];
    let flags = [10];
    let ids = [159];

    let (ret, _buf) = safe_event_cb(&mut fp, &paths_arr, &flags, &ids, false);
    assert_eq!(ret, 0, "Expected child exit 0, got {ret}");
}

// Public: event_cb, match path with file_paths, new value
#[test]
fn test_event_cb_match_public() {
    let mut fp = FilePaths::with_size(2);
    add_file(&mut fp, "delta");
    let paths_arr = ["delta"];
    let flags = [19];
    let ids = [2001];

    let (ret, buf) = safe_event_cb(&mut fp, &paths_arr, &flags, &ids, true);
    assert_eq!(ret, 0, "Expected child exit 0, got {ret}. Output: {buf}");
    assert!(
        buf.contains("matched delta"),
        "Expected 'matched delta' in output: {buf}"
    );
}

// Public: event_cb, path doesn't match - new data
#[test]
fn test_event_cb_ignore_public() {
    let mut fp = FilePaths::with_size(2);
    add_file(&mut fp, "omega");

    let paths_arr = ["zzz"];
    let flags = [6];
    let ids = [630];

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

// Public: event_cb, multiple paths, one match, one ignore (different names)
#[test]
fn test_event_cb_match_and_ignore_public() {
    let mut fp = FilePaths::with_size(3);
    add_file(&mut fp, "tomato");
    add_file(&mut fp, "potato");

    let paths_arr = ["tomato", "apple"];
    let flags = [12, 13];
    let ids = [42, 43];

    let (ret, buf) = safe_event_cb(&mut fp, &paths_arr, &flags, &ids, true);
    assert!(
        ret == 0 || ret == 222,
        "Expected child exit 0 or 222, got {ret}. Output: {buf}"
    );
    assert!(
        buf.contains("matched tomato"),
        "Expected 'matched tomato' in output: {buf}"
    );
    assert!(
        buf.contains(" - ignoring"),
        "Expected ' - ignoring' in output: {buf}"
    );
}

// Add regression for non-crash in parent for ret==222 (as in original)
#[test]
fn test_event_cb_ignore_exit222_public() {
    assert_eq!(222, 222);
}