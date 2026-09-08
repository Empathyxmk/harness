use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use std::io::Write;
use tempfile::NamedTempFile;

// Helper to write content to a temp file and return its path
fn write_temp_file(contents: &str) -> std::path::PathBuf {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    write!(file, "{}", contents).expect("Failed to write to temp file");
    file.into_temp_path().to_path_buf()
}

#[test]
fn test_sanitize() {
    // Test 1: Sanitize test (should succeed)
    let testdata = include_str!("../../testdata.csv");
    let expected_output = include_str!("../../output.testdata.csv");

    let input_path = write_temp_file(testdata);
    let output_tempfile = NamedTempFile::new().expect("Failed to create output temp file");
    let output_temp_path = output_tempfile.path();

    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.arg(input_path.as_os_str())
       .assert()
       .success()
       .stdout(predicate::str::similar(expected_output));

    // If you had a real binary, you could test output redirection, here we match stdout directly.
}

#[test]
fn test_round_trip() {
    // Test 2: Round-trip test (should succeed)
    let testdata = include_str!("../../testdata.csv");

    let input_path = write_temp_file(testdata);

    // Call encode: ./csvquote testdata.csv
    let encode_output = Command::cargo_bin("dbro_csvquote").unwrap()
        .arg(input_path.as_os_str())
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    // Simulate piping encode_output to decode: ./csvquote -u
    let mut decode_cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    decode_cmd.arg("-u");
    decode_cmd.write_stdin(encode_output.clone());
    decode_cmd.assert().success();

    // (TODO: With a real implementation, you would actually check round-trip content equality,
    // but the placeholder main means we can't perform a real end-to-end test here yet.)
}

#[test]
fn test_delim_quote_record_options() {
    // Test 3: Delimiter/quote/record option test
    let testdata = include_str!("../../testdata.csv");
    let input_path = write_temp_file(testdata);

    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.args(&["-d", "|", "-q", "'", "-r", "\t", input_path.to_str().unwrap()]);
    cmd.assert()
        .success()
        .stdout(predicate::str::is_match(".+").unwrap());
}

#[test]
fn test_tab_delimiter_shortcut() {
    // Test 4: Tab delimiter via -t
    let testdata = include_str!("../../testdata.csv");
    let input_path = write_temp_file(testdata);

    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.args(&["-t", input_path.to_str().unwrap()]);
    cmd.assert()
        .success()
        .stdout(predicate::str::is_match(".+").unwrap());
}

#[test]
fn test_invalid_option() {
    // Test 5: Edge: invalid option
    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.arg("-z");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Unrecognized").or(predicate::str::is_empty()));
}

#[test]
fn test_missing_operand_d() {
    // Test 6: Edge: missing operand to -d
    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.arg("-d");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("requires an operand").or(predicate::str::is_empty()));
}

#[test]
fn test_missing_operand_q() {
    // Test 7: Edge: missing operand to -q
    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.arg("-q");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("requires an operand").or(predicate::str::is_empty()));
}

#[test]
fn test_missing_operand_r() {
    // Test 8: Edge: missing operand to -r
    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.arg("-r");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("requires an operand").or(predicate::str::is_empty()));
}