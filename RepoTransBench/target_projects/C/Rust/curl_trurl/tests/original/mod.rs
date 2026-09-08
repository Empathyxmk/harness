//! This mod loads and runs original test cases (as per tests.json and tests.json.bak)
//!
//! The test runner below mimics, in Rust, the logic that was present in test.py,
//! by taking in the argument sets and expected outputs, spawning the binary and checking results.

use assert_cmd::Command;
use predicates::prelude::*;
use serde::Deserialize;
use serde_json::Value;
use std::fs;
use std::path::Path;

/// Describes one test case from the original suite.
#[derive(Debug, Deserialize)]
struct TestCase {
    input: TestInput,
    #[serde(default)]
    required: Option<Vec<String>>,
    #[serde(default)]
    encoding: Option<String>,
    expected: TestExpected,
}

#[derive(Debug, Deserialize)]
struct TestInput {
    arguments: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct TestExpected {
    #[serde(default)]
    stdout: Option<Value>,
    #[serde(default)]
    stderr: Option<Value>,
    returncode: i32,
}

fn get_trurl_bin_path() -> String {
    // For test purposes, use built binary at `target/debug/curl_trurl`
    if cfg!(windows) {
        "target/debug/curl_trurl.exe".to_string()
    } else {
        "target/debug/curl_trurl".to_string()
    }
}

/// Loads a JSON array file of test cases.
fn load_cases<P: AsRef<Path>>(path: P) -> Vec<TestCase> {
    let contents = fs::read_to_string(path).expect("Could not read test JSON file");
    serde_json::from_str(&contents).expect("Invalid JSON in test file")
}

// Helper for matching expected output, supporting string/array/bool
fn check_value(actual: &str, expected: &Option<Value>) -> bool {
    match expected {
        None => true,
        Some(Value::String(s)) => s == actual,
        Some(Value::Bool(b)) => {
            if *b {
                !actual.trim().is_empty()
            } else {
                actual.trim().is_empty()
            }
        }
        Some(Value::Array(_)) => {
            // If expected is an Array/struct, parse actual as JSON first
            match serde_json::from_str::<Value>(actual) {
                Ok(actual_json) => expected == &Some(actual_json),
                Err(_) => false,
            }
        }
        _ => false,
    }
}

#[test]
fn test_original_tests_json() {
    let trurl_bin = get_trurl_bin_path();
    let cases = load_cases("tests.json");
    for (idx, case) in cases.iter().enumerate() {
        let args: Vec<&str> = case.input.arguments.iter().map(|s| s.as_str()).collect();

        let mut cmd = Command::new(&trurl_bin);
        cmd.args(&args);
        let output = cmd.output().expect("Failed to run trurl binary");

        let stdout = String::from_utf8_lossy(&output.stdout).to_string();
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        let success = output.status.code().unwrap_or(-1);

        // Compare expected outputs
        let mut matched = true;
        matched &= check_value(&stdout, &case.expected.stdout);
        matched &= check_value(&stderr, &case.expected.stderr);

        if let Some(Value::Bool(expected_bool)) = &case.expected.stderr {
            // If true, expect any stderr output; if false, expect empty
            matched &= (*expected_bool && !stderr.trim().is_empty())
                || (!*expected_bool && stderr.trim().is_empty());
        }

        matched &= success == case.expected.returncode;

        if !matched {
            eprintln!(
                "\nTest [{} - {:?}]: FAILED\n  Args: {:?}\n  Expected: {:?}\n  Got: (code={})\n  STDOUT: {:?}\n  STDERR: {:?}\n",
                idx, case.input.arguments.get(0), &case.input.arguments, &case.expected, success, stdout, stderr
            );
        }
        assert!(
            matched,
            "Test case {} failed: \nExpected: {:?}\nSTDOUT: {}\nSTDERR: {}\nStatus: {}",
            idx,
            case.expected,
            stdout,
            stderr,
            success
        );
    }
}

#[test]
fn test_original_tests_json_bak() {
    let trurl_bin = get_trurl_bin_path();
    let cases = load_cases("tests.json.bak");
    for (idx, case) in cases.iter().enumerate() {
        let args: Vec<&str> = case.input.arguments.iter().map(|s| s.as_str()).collect();

        let mut cmd = Command::new(&trurl_bin);
        cmd.args(&args);
        let output = cmd.output().expect("Failed to run trurl binary");

        let stdout = String::from_utf8_lossy(&output.stdout).to_string();
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        let success = output.status.code().unwrap_or(-1);

        // Compare expected outputs
        let mut matched = true;
        matched &= check_value(&stdout, &case.expected.stdout);
        matched &= check_value(&stderr, &case.expected.stderr);

        if let Some(Value::Bool(expected_bool)) = &case.expected.stderr {
            matched &= (*expected_bool && !stderr.trim().is_empty())
                || (!*expected_bool && stderr.trim().is_empty());
        }

        matched &= success == case.expected.returncode;

        if !matched {
            eprintln!(
                "\nTest [{} - {:?}]: FAILED\n  Args: {:?}\n  Expected: {:?}\n  Got: (code={})\n  STDOUT: {:?}\n  STDERR: {:?}\n",
                idx, case.input.arguments.get(0), &case.input.arguments, &case.expected, success, stdout, stderr
            );
        }
        assert!(
            matched,
            "Test case {} failed: \nExpected: {:?}\nSTDOUT: {}\nSTDERR: {}\nStatus: {}",
            idx,
            case.expected,
            stdout,
            stderr,
            success
        );
    }
}