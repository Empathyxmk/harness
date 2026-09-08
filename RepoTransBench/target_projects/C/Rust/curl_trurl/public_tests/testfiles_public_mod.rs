//! Additional tests for public test file "testfiles_public", using the simplified txt spec files.
//! We parse and replicate the logic of those test files line-by-line.

use assert_cmd::Command;
use std::fs;

/// Performs a simple split using a testfiles_public style test file:
/// Each block starts with "input:" line and an "expected:" line.
/// Comments (lines starting with #) and empty lines are ignored.
fn run_testfile(path: &str) {
    let content = fs::read_to_string(path).expect("couldn't read public testfile");
    let mut lines = content.lines().peekable();
    while let Some(line) = lines.next() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if line.starts_with("input:") {
            let input = line["input:".len()..].trim();
            let mut expected = None;
            while let Some(nline) = lines.peek() {
                let nline = nline.trim();
                if nline.is_empty() || nline.starts_with('#') {
                    lines.next();
                } else if nline.starts_with("expected:") {
                    expected = Some(nline["expected:".len()..].trim());
                    lines.next();
                    break;
                } else {
                    break;
                }
            }
            // Now run the test with input+expected
            let input_args: Vec<&str> = shell_words::split(input).unwrap();
            let mut cmd = Command::cargo_bin("curl_trurl").unwrap();
            cmd.args(&input_args);
            let output = cmd.output().expect("Failed to run curl_trurl bin");
            let stdout = String::from_utf8_lossy(&output.stdout).to_string();
            let stderr = String::from_utf8_lossy(&output.stderr).to_string();
            let code = output.status.code().unwrap_or(-1);

            // Parse expected string (comma-separated "k=v" pairs or single "path=val")
            if let Some(expects) = expected {
                for item in expects.split(',') {
                    let kv = item.trim();
                    if kv.is_empty() {
                        continue;
                    }
                    let mut split = kv.splitn(2, '=');
                    let key = split.next().unwrap().trim();
                    let val = split.next().unwrap_or("").trim();
                    let found = stdout.contains(val);
                    assert!(
                        found,
                        "FAILED public test: [{}]:\n  Input: {}\n  Expected {}={}\n  STDOUT: {}\n  STDERR: {}",
                        path,
                        input,
                        key,
                        val,
                        stdout,
                        stderr
                    );
                }
            } else {
                assert!(false, "Public testfile {}: Input '{}' did not have an expected result!", path, input);
            }
        }
    }
}

#[test]
fn testfile_public_0000() {
    run_testfile("testfiles_public/test_public_0000.txt");
}
#[test]
fn testfile_public_0001() {
    run_testfile("testfiles_public/test_public_0001.txt");
}
#[test]
fn testfile_public_0002() {
    run_testfile("testfiles_public/test_public_0002.txt");
}