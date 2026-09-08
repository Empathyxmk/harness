use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_trim_paired_args() {
    let exe = Command::cargo_bin("najoshi_sickle").unwrap();

    // sickle pe with missing required args
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["pe"]);
    cmd.assert().failure().stderr(predicate::str::contains("Usage"));

    // sickle pe with single input (missing pair input should fail)
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["pe", "-f", "test/test.f.fastq", "-t", "sanger", "-o", "out1.fastq", "-p", "out2.fastq", "-s", "single.fastq"]);
    cmd.assert().failure().stderr(predicate::str::contains("pair").or(predicate::str::contains("Usage")));

    // sickle pe with all required args
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["pe", "-f", "test/test.f.fastq", "-r", "test/test.r.fastq", "-t", "sanger", "-o", "out1.fastq", "-p", "out2.fastq", "-s", "single.fastq"]);
    cmd.assert().success();
}