//! Public test cases from public test specs (tests_public.json and testfiles_public).

use assert_cmd::Command;
use predicates::prelude::*;
use serde::Deserialize;
use serde_json::Value;
use std::fs;
use std::path::Path;

#[derive(Debug, Deserialize)]
struct TestCase {
    input: TestInput,
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
    if cfg!(windows) {
        "target/debug/curl_trurl.exe".to_string()
    } else {
        "target/debug/curl_trurl".to_string()
    }
}

fn load_cases<P: AsRef<Path>>(path: P) -> Vec<TestCase> {
    let contents = fs::read_to_string(path).expect("Could not read test JSON file");
    serde_json::from_str(&contents).expect("Invalid JSON in test file")
}

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
            match serde_json::from_str::<Value>(actual) {
                Ok(actual_json) => expected == &Some(actual_json),
                Err(_) => false,
            }
        }
        _ => false,
    }
}

#[test]
fn test_public_json_cases() {
    let trurl_bin = get_trurl_bin_path();
    let cases = load_cases("tests_public.json");
    for (idx, case) in cases.iter().enumerate() {
        let args: Vec<&str> = case.input.arguments.iter().map(|s| s.as_str()).collect();

        let mut cmd = Command::new(&trurl_bin);
        cmd.args(&args);
        let output = cmd.output().expect("Failed to run trurl binary");

        let stdout = String::from_utf8_lossy(&output.stdout).to_string();
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        let success = output.status.code().unwrap_or(-1);

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
            "Public test case {} failed: \nExpected: {:?}\nSTDOUT: {}\nSTDERR: {}\nStatus: {}",
            idx,
            case.expected,
            stdout,
            stderr,
            success
        );
    }
}