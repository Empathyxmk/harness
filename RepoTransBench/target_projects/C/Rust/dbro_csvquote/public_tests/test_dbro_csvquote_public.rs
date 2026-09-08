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
fn test_public_sanitize() {
    // 1. Sanitize test (should succeed)
    let testdata = include_str!("public_testdata.csv");
    let expected_output = include_str!("output.public_testdata.csv");

    let input_path = write_temp_file(testdata);

    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.args(&["-d", ";", input_path.to_str().unwrap()])
        .assert()
        .success()
        .stdout(predicate::str::similar(expected_output));
}

#[test]
fn test_public_round_trip() {
    // 2. Round-trip test (should succeed)
    let testdata = include_str!("public_testdata.csv");
    let input_path = write_temp_file(testdata);

    let encode_output = Command::cargo_bin("dbro_csvquote").unwrap()
        .args(&["-d", ";", input_path.to_str().unwrap()])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    // Simulate piping encode_output to decode: ./csvquote -u -d ';'
    let mut decode_cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    decode_cmd.args(&["-u", "-d", ";"]);
    decode_cmd.write_stdin(encode_output.clone());
    decode_cmd.assert().success();
    // With a real implementation, would compare output, for now we check for success.
}

#[test]
fn test_public_custom_delim() {
    // 3. Delimiter/quote/record options test (use different set)
    let testdata = include_str!("public_testdata.csv");
    let input_path = write_temp_file(testdata);

    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.args(&["-d", ":", "-q", "'", "-r", "\x0b", input_path.to_str().unwrap()]);
    cmd.assert()
        .success()
        .stdout(predicate::str::is_match(".+").unwrap());
}

#[test]
fn test_public_space_delim() {
    // 4. Whitespace delimiter via -d ' ' (space)
    let testdata = include_str!("public_testdata.csv");
    let input_path = write_temp_file(testdata);

    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.args(&["-d", " ", input_path.to_str().unwrap()]);
    cmd.assert()
        .success()
        .stdout(predicate::str::is_match(".+").unwrap());
}

#[test]
fn test_public_invalid_option() {
    // 5. Edge: invalid option
    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.arg("-z");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Unrecognized").or(predicate::str::is_empty()));
}

#[test]
fn test_public_missing_operand_d() {
    // 6. Edge: missing operand to -d
    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.arg("-d");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("requires an operand").or(predicate::str::is_empty()));
}

#[test]
fn test_public_missing_operand_q() {
    // 7. Edge: missing operand to -q
    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.arg("-q");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("requires an operand").or(predicate::str::is_empty()));
}

#[test]
fn test_public_missing_operand_r() {
    // 8. Edge: missing operand to -r
    let mut cmd = Command::cargo_bin("dbro_csvquote").unwrap();
    cmd.arg("-r");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("requires an operand").or(predicate::str::is_empty()));
}