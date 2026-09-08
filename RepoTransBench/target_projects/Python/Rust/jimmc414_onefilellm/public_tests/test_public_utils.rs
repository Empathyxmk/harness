// Rust translation of public_tests/test_public_utils.py

use std::fs::{self, File};
use std::io::Write;
use tempfile::tempdir;
use onefilellm::utils::*;

#[test]
fn test_safe_file_read_utf8_and_fallback_public() {
    let dir = tempdir().unwrap();
    let p = dir.path().join("foo.txt");
    let data = "Testing äßü";
    fs::write(&p, data).unwrap();
    assert_eq!(safe_file_read(p.to_str().unwrap()), data);

    let p2 = dir.path().join("bar.txt");
    let text = "niño";
    {
        let mut f = File::create(&p2).unwrap();
        f.write_all(text.as_bytes()).unwrap();
    }
    assert_eq!(safe_file_read(p2.to_str().unwrap()), text);
}

#[test]
fn test_detect_text_format_public() {
    let tests = [
        (r#"{"foo": 42}"#, "json"),
        ("[100, 200, 300]", "json"),
        ("<HTML>Tag</HTML>", "html"),
        ("<!DOCTYPE HTML>", "html"),
        ("<span>public</span>", "html"),
        ("## Subheader\nSome text", "markdown"),
        ("*item*", "markdown"),
        ("A random sentence", "text"),
        (" ", "text"),
        ("\n\n", "text"),
    ];
    for (txt, expected) in tests.iter() {
        assert_eq!(detect_text_format(txt), *expected);
    }
}

#[test]
fn test_parse_as_plaintext_and_markdown_public() {
    let s = "xyz";
    assert_eq!(parse_as_plaintext(s), s);
    assert_eq!(parse_as_markdown(s), s);
}

#[test]
fn test_parse_as_json_and_yaml_and_html_public() {
    let s_json = r#"{"x": 99, "y": 88}"#;
    assert_eq!(parse_as_json(s_json), s_json);

    let html = "<html><body>World</body></html>";
    assert!(parse_as_html(html).contains("World"));
}

#[test]
fn test_is_same_domain_public() {
    assert!(is_same_domain("https://b.com/page", "https://b.com/y"));
    assert!(!is_same_domain("https://b.com", "https://sub.b.com/a"));
    assert!(is_same_domain("http://b.com/xy", "https://b.com/zzz"));
}

#[test]
fn test_is_within_depth_public() {
    assert!(is_within_depth("https://b.com", "https://b.com/abc/def", 2));
    assert!(!is_within_depth("https://b.com", "https://b.com/a/b/c/d", 3));
    assert!(!is_within_depth("http://b.com", "https://b.com/a/b", 1));
}

#[test]
fn test_is_excluded_file_public() {
    assert!(!is_excluded_file("/bar/src/main.py"));
    assert!(is_excluded_file("/bar/node_modules/script.js"));
    assert!(is_excluded_file("/bar/.git/description"));
}

#[test]
fn test_is_allowed_filetype_public() {
    assert!(is_allowed_filetype("main.go"));
    assert!(is_allowed_filetype("foo.md"));
    assert!(!is_allowed_filetype("file.dll"));
    assert!(is_allowed_filetype("file.MD"));
}

#[test]
fn test_escape_xml_public() {
    let raw = "<public>&amp;</public>";
    assert_eq!(escape_xml(raw), raw);
}