use pdf_redactor_rs::pdf_redactor::{RedactorOptions, redactor};
use regex::Regex;

#[test]
fn test_basic_redaction() {
    let mut options = RedactorOptions::default();
    options.content_filters = vec![
        (
            Regex::new(r"\b654-32-1987\b").unwrap(),
            Box::new(|_m: &str| "[REDACTED-ID]".to_string()),
        ),
    ];
    let pdf_in = b"%PDF-1.4\n% Public test: secret12345 replaced\nxyz 654-32-1987 zyx\n%%EOF".to_vec();
    let mut out = vec![];
    redactor(&mut options, Some(pdf_in.clone()), &mut out).unwrap();
    assert!(out.contains(&b'['));
    let s = String::from_utf8_lossy(&out);
    assert!(s.contains("[REDACTED-ID]"));
}

#[test]
fn test_unicode_filter() {
    let mut options = RedactorOptions::default();
    options.content_filters = vec![(
        Regex::new(r"\b88-99-7766\b").unwrap(),
        Box::new(|_m: &str| "<REMOVED>".to_string()),
    )];
    let pdf_in = "%PDF-1.4\nUnusual symbol: §\nID 88-99-7766\n%%EOF".as_bytes().to_vec();
    let mut out = vec![];
    redactor(&mut options, Some(pdf_in.clone()), &mut out).unwrap();
    let s = String::from_utf8_lossy(&out);
    assert!(s.contains("<REMOVED>"));
}

#[test]
fn test_multiline_filter() {
    let mut options = RedactorOptions::default();
    options.content_filters = vec![(
        Regex::new(r"222-33-4444").unwrap(),
        Box::new(|_m: &str| "*****".to_string()),
    )];
    let pdf_in = b"%PDF-1.4\nFirstLine\nID: 222-33-4444\nSecondLine\n%%EOF".to_vec();
    let mut out = vec![];
    redactor(&mut options, Some(pdf_in.clone()), &mut out).unwrap();
    let s = String::from_utf8_lossy(&out);
    assert!(s.contains("*****"));
}