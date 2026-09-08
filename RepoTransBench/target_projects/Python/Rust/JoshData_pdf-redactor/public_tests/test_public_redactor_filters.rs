use pdf_redactor_rs::pdf_redactor::{RedactorOptions, redactor};
use regex::Regex;

#[test]
fn test_filter_callable_replacement() {
    let mut options = RedactorOptions::default();
    let repl = |_: &str| "MASKED".to_string();
    options.content_filters = vec![(Regex::new(r"\d{3}-\d{2}-\d{4}").unwrap(), Box::new(repl))];
    let pdf_in = b"%PDF-1.4\nSSN 159-46-2879\n%%EOF".to_vec();
    let mut out = vec![];
    redactor(&mut options, Some(pdf_in.clone()), &mut out).unwrap();
    let s = String::from_utf8_lossy(&out);
    assert!(s.contains("MASKED"));
}

#[test]
fn test_filter_non_callable_replacement() {
    let mut options = RedactorOptions::default();
    options.content_filters = vec![
        (Regex::new("Angela Bailey").unwrap(), Box::new(|_m| "AnonName".to_string())),
    ];
    let pdf_in = b"%PDF-1.4\nName: Angela Bailey\n%%EOF".to_vec();
    let mut out = vec![];
    redactor(&mut options, Some(pdf_in.clone()), &mut out).unwrap();
    let s = String::from_utf8_lossy(&out);
    assert!(s.contains("AnonName"));
}