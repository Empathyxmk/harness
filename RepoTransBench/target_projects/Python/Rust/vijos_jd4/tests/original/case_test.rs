use vijos_jd4::case::{read_cases, Case};
use std::fs::File;
use std::path::PathBuf;
use std::io::{Read, Cursor};

#[test]
fn test_legacy_case() {
    let cases = read_cases(Cursor::new(b"dummy_zip"));
    assert_eq!(cases.len(), 10);
    for case in cases {
        assert_eq!(case.score, 10);
        // Test dummy data
        assert_eq!(case.input, "1 2");
        assert_eq!(case.output, "3");
    }
}

#[test]
fn test_yaml_case() {
    let cases = read_cases(Cursor::new(b"dummy_yaml"));
    assert_eq!(cases.len(), 10);
    for case in cases {
        assert_eq!(case.score, 10);
        assert_eq!(case.input, "1 2");
        assert_eq!(case.output, "3");
    }
}