use std::collections::HashMap;
use std::fs;
use tempfile::NamedTempFile;
use serde_json::Value;

#[test]
fn test_mkexcel_creates_xls() {
    // Prepare the data record
    let mut record = HashMap::new();
    record.insert("foo".to_string(), Value::from(42));
    record.insert("bar".to_string(), Value::from("baz"));
    let data = vec![record];

    // Create a temporary file path for the xls file
    let tmpfile = NamedTempFile::new().expect("failed to create temp file");
    let path = tmpfile.path().to_str().unwrap().to_owned() + ".xls";

    // Call the mkexcel function
    // (Assuming you implemented or stubbed this function in src/utils.rs)
    crate::utils::mkexcel(&data, &path).expect("mkexcel failed");

    // Check the file now exists and is not empty
    assert!(fs::metadata(&path).is_ok());
    let filesize = fs::metadata(&path).unwrap().len();
    assert!(filesize > 0, "Generated xls file is empty");
}