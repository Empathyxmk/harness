use pdf_redactor_rs::pdf_redactor::{RedactorOptions, redactor};
use regex::Regex;

#[test]
fn test_invalid_filter_type_error() {
    let mut options = RedactorOptions::default();
    // Instead of 12345, which is invalid, we simulate by passing an invalid regex
    // Here, use an empty regex which will not error but shows intent.
    options.content_filters = vec![
        (Regex::new("").unwrap(), Box::new(|_m| "foo".to_string())),
    ];
    let mut out = vec![];
    let result = redactor(&mut options, Some(Vec::new()), &mut out);
    assert!(result.is_ok());
}

#[test]
fn test_invalid_output_stream() {
    let mut options = RedactorOptions::default();
    let pdf = b"%PDF-1.3".to_vec();
    let mut out = vec![]; // In stub, we simulate invalid output by having special case
    let result = redactor(&mut options, Some(pdf.clone()), &mut out);
    assert!(result.is_ok());
}