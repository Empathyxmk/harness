use assert_cmd::prelude::*;
use predicates::prelude::*;
use std::process::Command;

#[test]
fn test_sickle_args() {
    // sickle with no args (should show usage and return error)
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.assert().failure().stderr(predicate::str::contains("Usage").or(predicate::str::contains("usage")));

    // sickle with nonsense command (should show usage and return error)
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.arg("nonsense")
        .assert()
        .failure()
        .stderr(predicate::str::contains("Usage").or(predicate::str::contains("usage")));

    // sickle --help (should show usage and exit 0)
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("Usage: sickle"));

    // sickle --version (should show version and exit 0)
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.arg("--version")
        .assert()
        .success()
        .stdout(predicate::str::contains("sickle version"));
}