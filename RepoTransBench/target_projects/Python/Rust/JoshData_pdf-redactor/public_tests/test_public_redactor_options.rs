use pdf_redactor_rs::pdf_redactor::RedactorOptions;
use std::collections::HashMap;

#[test]
fn test_metadata_defaults() {
    let mut meta = HashMap::new();
    meta.insert("Title".to_string(), "PublicTitle".to_string());
    meta.insert("Subject".to_string(), "PublicSubj".to_string());
    meta.insert("Author".to_string(), "AuthorPerson".to_string());
    let options = RedactorOptions::from_metadata(meta.clone());
    assert_eq!(options.metadata["Title"], "PublicTitle");
    assert_eq!(options.metadata["Subject"], "PublicSubj");
    assert_eq!(options.metadata["Author"], "AuthorPerson");
}

#[test]
fn test_options_filters_list() {
    use regex::Regex;
    let mut options = RedactorOptions::default();
    options.content_filters = vec![
        (Regex::new(r"\\d{2}-\\d{2}-\\d{4}").unwrap(), Box::new(|_m| "REDACT".to_string())),
        (Regex::new("SecretWord").unwrap(), Box::new(|_m| "VisibleWord".to_string())),
    ];
    assert_eq!(options.content_filters.len(), 2);
    assert_eq!(
        (options.content_filters.get(1).unwrap().1)("dummy"),
        "VisibleWord"
    );
}