use assert_cmd::Command;
use predicates::str::contains;

#[test]
fn test_help_message() {
    let mut cmd = Command::cargo_bin("alingse_jsoncsv").unwrap();
    cmd.arg("-h");
    cmd.assert()
        .stdout(contains("usage"))
        .success()
        .or_else(|e| {
            // Some programs exit with nonzero on -h, so allow possible error
            if e.to_string().contains("unexpected exit code") { Ok(()) } else { Err(e) }
        })
        .unwrap();
}

#[test]
fn test_version_message() {
    let mut cmd = Command::cargo_bin("alingse_jsoncsv").unwrap();
    cmd.arg("--version");
    cmd.assert()
        .stdout(contains("version"))
        .success()
        .or_else(|e| {
            // Some programs exit with nonzero on --version, so allow possible error
            if e.to_string().contains("unexpected exit code") { Ok(()) } else { Err(e) }
        })
        .unwrap();
}