//! Translated from tests/test_examples_argtable_public.c
//! These tests use `assert_cmd` to spawn binaries and assert on output.

use assert_cmd::Command;
use predicates::str::contains;

const EXAMPLES_ECHO: &str = "./examples/echo";
const EXAMPLES_TESTARGTABLE3: &str = "./examples/testargtable3";

#[test]
fn test_echo_public() {
    // Single string, with -n
    Command::new(EXAMPLES_ECHO)
        .args(&["-n", "HelloWorld"])
        .assert()
        .success()
        .stdout(contains("option -n = YES"))
        .stdout(contains("HelloWorld"));

    // Multiple strings, with -E (not -e)
    Command::new(EXAMPLES_ECHO)
        .args(&["-E", "This", "is", "public"])
        .assert()
        .success()
        .stdout(contains("option -E = YES"))
        .stdout(contains("This"))
        .stdout(contains("public"));

    // --version
    Command::new(EXAMPLES_ECHO)
        .arg("--version")
        .assert()
        .stdout(contains("echo v3"));

    // --help
    Command::new(EXAMPLES_ECHO)
        .arg("--help")
        .assert()
        .stdout(contains("Usage: echo"))
        .stdout(contains("do not output the trailing newline"));

    // Error: unknown option
    Command::new(EXAMPLES_ECHO)
        .arg("--notarealopt")
        .assert()
        .stdout(contains("Try 'echo --help' for more information."));
}

#[test]
fn test_testargtable3_public() {
    // Simple file and -b
    Command::new(EXAMPLES_TESTARGTABLE3)
        .args(&["-b", "input1.txt"])
        .assert()
        .success();

    // Output file and scalar flag
    Command::new(EXAMPLES_TESTARGTABLE3)
        .args(&["-o", "outfile.txt", "--scalar=24", "something.data"])
        .assert()
        .success();

    // Help and version
    Command::new(EXAMPLES_TESTARGTABLE3)
        .arg("--help")
        .assert()
        .stdout(contains("Usage: testargtable2.exe"));

    Command::new(EXAMPLES_TESTARGTABLE3)
        .arg("--version")
        .assert()
        .stdout(contains("testargtable2.exe v3"));

    // Error: missing required file parameter
    Command::new(EXAMPLES_TESTARGTABLE3)
        .arg("-a")
        .assert()
        .stdout(contains("Try 'testargtable2.exe --help' for more information."));
}