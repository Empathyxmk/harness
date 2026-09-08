//! Rust translation of antirez_aocla test_aocla_coverage.c
//! Test: run with dummy input file name, should "run" successfully

use antirez_aocla::aocla_main;

/// Coverage: call with dummy input file name, expect exit code 0.
#[test]
fn test_dummy_input_file_case() {
    // Simulate argv: program name, dummy filename
    let argv = ["progname", "dummy.aocla"];
    let rc = aocla_main(2, &argv);
    assert_eq!(
        rc, 0,
        "FAIL: Expected exit code 0 for input file present, got {}",
        rc
    );
    println!("PASS: dummy input file case");
}