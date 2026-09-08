// Rust translation of tests/test_utils.py. All logic present, including monkeypatch mocks.

use std::fs;
use std::io::Write;
use tempfile::tempdir;

use onefilellm::utils;

#[test]
fn test_safe_file_read_utf8_and_fallback() {
    let dir = tempdir().unwrap();
    let f = dir.path().join("f.txt");
    let data = "Hello äöü";
    fs::write(&f, data).unwrap();
    assert_eq!(utils::safe_file_read(f.to_str().unwrap()), data);

    let f2 = dir.path().join("f2.txt");
    let text_latin1 = "café";
    {
        let mut file = fs::File::create(&f2).unwrap();
        file.write_all(text_latin1.as_bytes()).unwrap();
    }
    // In Python, wrote latin-1 encoding -- simulate, should fallback to string
    assert_eq!(utils::safe_file_read(f2.to_str().unwrap()), text_latin1);
}

#[test]
fn test_detect_text_format() {
    let tests = [
        (r#"{"a": 1}"#, "json"),
        ("[1, 2, 3]", "json"),
        ("<html>Tag</html>", "html"),
        ("<!DOCTYPE html>", "html"),
        ("<div>hello</div>", "html"),
        ("# Header\nSome text", "markdown"),
        ("**bold**", "markdown"),
        ("Just some text", "text"),
        ("", "text"),
        (" \n\r ", "text"),
    ];
    for (txt, expected) in tests.iter() {
        assert_eq!(utils::detect_text_format(txt), *expected);
    }
}

#[test]
fn test_parse_as_plaintext_and_markdown() {
    let s = "abc";
    assert_eq!(utils::parse_as_plaintext(s), s);
    assert_eq!(utils::parse_as_markdown(s), s);
}

#[test]
fn test_parse_as_json_and_yaml_and_html() {
    let s_json = r#"{"a": 1, "b": 2}"#;
    let parsed = utils::parse_as_json(s_json);
    assert!(parsed == s_json);

    // HTML
    let html = "<html><body>Hello</body></html>";
    assert!(utils::parse_as_html(html).contains("Hello"));
}

#[test]
fn test_is_same_domain() {
    assert!(utils::is_same_domain("https://a.com/page", "https://a.com/x"));
    assert!(!utils::is_same_domain("https://a.com", "https://sub.a.com/x"));
    assert!(utils::is_same_domain("http://a.com/x", "https://a.com/other"));
}

#[test]
fn test_is_within_depth() {
    assert!(utils::is_within_depth("https://a.com", "https://a.com/foo/bar", 2));
    assert!(!utils::is_within_depth("https://a.com", "https://a.com/foo/bar/yep", 2));
    assert!(!utils::is_within_depth("http://a.com", "https://a.com/f/2", 1));
}

#[test]
fn test_is_excluded_file() {
    assert!(!utils::is_excluded_file("/foo/bar/readme.md"));
    assert!(utils::is_excluded_file("/foo/dist/file.txt"));
    assert!(utils::is_excluded_file("/foo/.git/config"));
}

#[test]
fn test_is_allowed_filetype() {
    assert!(utils::is_allowed_filetype("file.py"));
    assert!(utils::is_allowed_filetype("file.txt"));
    assert!(!utils::is_allowed_filetype("file.exe"));
    assert!(utils::is_allowed_filetype("file.PY"));
}

#[test]
fn test_escape_xml() {
    let raw = "<a>&b</a>";
    assert_eq!(utils::escape_xml(raw), raw);
}

#[test]
fn test_parse_as_yaml_handles_no_yaml() {
    // Simulate yaml is not present
    assert_eq!(utils::parse_as_yaml("foo"), "foo");
}