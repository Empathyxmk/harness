// Rust translation of Python: tests/test_s3_pit_restore_smoke.py

use std::process::{Command, Stdio};
use std::str;

fn python_bin() -> String {
    // Try to get an appropriate python binary, fallback to "python3".
    std::env::var("PYTHON").unwrap_or_else(|_| "python3".to_string())
}

/// Check --help output and exit code
#[test]
fn test_s3_pit_restore_help() {
    let output = Command::new(python_bin())
        .arg("s3-pit-restore")
        .arg("--help")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output()
        .expect("failed to run s3-pit-restore --help");
    let stdout = String::from_utf8_lossy(&output.stdout).to_lowercase();
    assert!(stdout.contains("usage"), "stdout did not contain 'usage': {stdout}");
    assert_eq!(output.status.code(), Some(0), "exit code not 0");
}

/// If -b/--bucket missing, exit code is 2 and show error.
#[test]
fn test_s3_pit_restore_missing_bucket() {
    let output = Command::new(python_bin())
        .arg("s3-pit-restore")
        .arg("--version")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output()
        .expect("failed to run s3-pit-restore --version");
    assert_eq!(output.status.code(), Some(2), "exit code not 2");
    let stderr = String::from_utf8_lossy(&output.stderr).to_lowercase();
    assert!(
        stderr.contains("required") || stderr.contains("bucket"),
        "stderr did not mention 'required' or 'bucket': {stderr}"
    );
}