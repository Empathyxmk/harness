// Rust translation of Python: public_tests/test_public_s3_pit_restore_smoke.py

use std::process::{Command, Stdio};
use std::str;

fn python_bin() -> String {
    // Try to get an appropriate python binary, fallback to "python3".
    std::env::var("PYTHON").unwrap_or_else(|_| "python3".to_string())
}

/// Check output for --version argument (-V) (should exit code 2, mention bucket)
#[test]
fn test_s3_pit_restore_version_public() {
    let output = Command::new(python_bin())
        .arg("s3-pit-restore")
        .arg("-V")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output()
        .expect("failed to run s3-pit-restore -V");
    assert_eq!(output.status.code(), Some(2), "exit code not 2");
    let stderr = String::from_utf8_lossy(&output.stderr).to_lowercase();
    assert!(
        stderr.contains("required") || stderr.contains("bucket"),
        "stderr did not mention 'required' or 'bucket': {stderr}"
    );
}

/// Invalid argument (e.g., --notarealarg) produces exit code 2 and usage/error in stderr.
#[test]
fn test_s3_pit_restore_invalid_arg_public() {
    let output = Command::new(python_bin())
        .arg("s3-pit-restore")
        .arg("--notarealarg")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output()
        .expect("failed to run s3-pit-restore --notarealarg");
    assert_eq!(output.status.code(), Some(2), "exit code not 2");
    let stderr = String::from_utf8_lossy(&output.stderr).to_lowercase();
    assert!(
        stderr.contains("usage") || stderr.contains("error"),
        "stderr did not mention 'usage' or 'error': {stderr}"
    );
}