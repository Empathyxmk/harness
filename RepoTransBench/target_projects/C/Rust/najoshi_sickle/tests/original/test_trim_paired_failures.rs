use assert_cmd::Command;

#[test]
fn test_trim_paired_failures() {
    let exe = Command::cargo_bin("najoshi_sickle").unwrap();

    // sickle pe with output as gzip
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["pe", "-f", "test/test.f.fastq", "-r", "test/test.r.fastq", "-t", "sanger", "-o", "o1.fastq", "-p", "o2.fastq", "-s", "s1.fastq", "-g"]);
    cmd.assert().success();

    // sickle pe with no-fiveprime and quiet
    let mut cmd = Command::cargo_bin("najoshi_sickle").unwrap();
    cmd.args(&["pe", "-f", "test/test.f.fastq", "-r", "test/test.r.fastq", "-t", "sanger", "-o", "o1.fastq", "-p", "o2.fastq", "-s", "s1.fastq", "-x", "--quiet"]);
    cmd.assert().success();
}