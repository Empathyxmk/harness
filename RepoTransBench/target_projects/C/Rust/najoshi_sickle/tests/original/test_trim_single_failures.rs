use assert_cmd::Command;
use std::fs::File;
use std::io::Write;

#[test]
fn test_trim_single_failures() {
    let mut tmp_n = File::create("test/tmp_n.fastq").unwrap();
    writeln!(tmp_n, "@seq1\nACGNTAAA\n+\nIIIIIIII").unwrap();

    // sickle se with truncated N
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["se", "-f", "test/tmp_n.fastq", "-t", "sanger", "-o", "out.fastq", "-n"]);
    cmd.assert().success();

    // sickle se with quiet option
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["se", "-f", "test/test.fastq", "-t", "sanger", "-o", "out.fastq", "--quiet"]);
    cmd.assert().success();

    // sickle se with no-fiveprime
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["se", "-f", "test/test.fastq", "-t", "sanger", "-o", "out.fastq", "-x"]);
    cmd.assert().success();

    std::fs::remove_file("out.fastq").ok();
    std::fs::remove_file("test/tmp_n.fastq").ok();
}