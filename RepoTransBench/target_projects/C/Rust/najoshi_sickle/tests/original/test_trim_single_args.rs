use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_trim_single_args() {
    let exe = Command::cargo_bin("najoshi_sickle").unwrap();

    // sickle se with missing required args (should show usage and error)
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["se"]);
    cmd.assert().failure().stderr(predicate::str::contains("Usage"));

    // sickle se with invalid qual-type
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["se", "-f", "test/test.fastq", "-t", "notqual", "-o", "out.fastq"]);
    cmd.assert().failure().stderr(predicate::str::contains("Usage").or(predicate::str::contains("invalid")));

    // sickle se with negative quality threshold
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["se", "-f", "test/test.fastq", "-t", "sanger", "-o", "out.fastq", "-q", "-1"]);
    cmd.assert().failure();

    // sickle se with negative length threshold
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["se", "-f", "test/test.fastq", "-t", "sanger", "-o", "out.fastq", "-l", "-5"]);
    cmd.assert().failure();

    // sickle se with minimum args (happy path)
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["se", "-f", "test/test.fastq", "-t", "sanger", "-o", "out.fastq"]);
    cmd.assert().success();
}