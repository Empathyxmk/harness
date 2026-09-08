use std::collections::HashMap;
use tempfile::NamedTempFile;
use std::fs;

#[test]
fn test_public_mkexcel_generates_xls() {
    // Prepare test data
    let mut r = HashMap::new();
    r.insert("alpha".to_string(), serde_json::json!(999));
    r.insert("beta".to_string(), serde_json::json!("gee"));
    let data = vec![r];

    // Create temporary file with .xls extension
    let tmpfile = NamedTempFile::new().unwrap();
    let xls_path = format!("{}.xls", tmpfile.path().to_string_lossy());

    crate::utils::mkexcel(&data, &xls_path).expect("mkexcel failed");

    // Assert file exists and is non-empty
    assert!(fs::metadata(&xls_path).is_ok());
    assert!(fs::metadata(&xls_path).unwrap().len() > 0);
}