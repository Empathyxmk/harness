use serde_json::json;
use std::fs::{self, File};
use std::io::Write;
use tempfile::NamedTempFile;

#[test]
fn test_dumptool_json_output() {
    // Emulate: jsoncsv.dumptool.dumps() or dumps to tmp file
    let records = vec![
        json!({"foo": 1, "bar": "baz"}),
        json!({"foo": 2, "bar": "qux"})
    ];

    let mut tmpfile = NamedTempFile::new().unwrap();
    let path = tmpfile.path().to_str().unwrap();
    // Write records as JSON lines to tmpfile
    for obj in &records {
        writeln!(tmpfile, "{}", obj).unwrap();
    }
    tmpfile.flush().unwrap();

    // Now, read back and check lines
    let content = fs::read_to_string(path).unwrap();
    let lines: Vec<&str> = content.trim().split('\n').collect();

    assert_eq!(lines.len(), 2);
    assert_eq!(serde_json::from_str::<serde_json::Value>(lines[0]).unwrap(), records[0]);
    assert_eq!(serde_json::from_str::<serde_json::Value>(lines[1]).unwrap(), records[1]);
}