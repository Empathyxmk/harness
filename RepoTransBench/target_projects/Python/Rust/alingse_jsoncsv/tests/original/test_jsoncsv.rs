use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;

use alingse_jsoncsv::mainmod;

fn make_temp_file_with_content(dir: &PathBuf, filename: &str, content: &str) -> PathBuf {
    let file_path = dir.join(filename);
    let mut file = File::create(&file_path).expect("Failed to create file");
    file.write_all(content.as_bytes()).expect("Failed to write content");
    file_path
}

#[test]
fn test_main_expand() {
    // Create a temporary directory for the test
    let tempdir = tempfile::tempdir().expect("Could not create temp dir");
    let dir = tempdir.path().to_path_buf();

    let infile = make_temp_file_with_content(&dir, "input.json", r#"[{"a": 1}, {"a": 2}]"#);
    let outfile = dir.join("output.csv");

    let args = vec![
        "expand".to_string(),
        infile.to_str().unwrap().to_string(),
        "-o".to_string(),
        outfile.to_str().unwrap().to_string(),
    ];
    let result = mainmod::main(args);
    
    // If main returns a Result, we should assert success
    // If it does not, ignore result or check for type/unit.

    // Assert that outfile exists
    assert!(outfile.exists(), "Output CSV was not created");

    // Read file contents
    let out = fs::read_to_string(&outfile).expect("Failed to read output CSV");
    assert!(out.contains("a"), "CSV header 'a' missing");
    assert!(out.contains("1"), "CSV value '1' missing");
    assert!(out.contains("2"), "CSV value '2' missing");
}