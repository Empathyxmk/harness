//! Rust translation of antirez_aocla test_aocla_basic.c
//! Basic smoke test: run with no args, should print usage

use antirez_aocla::aocla_main;

/// Basic: call with no input arguments, expect exit code 1.
#[test]
fn test_no_input_file_case() {
    // Simulate argv: just program name
    let argv = ["progname"];
    let rc = aocla_main(1, &argv);
    assert_eq!(
        rc, 1,
        "FAIL: Expected exit code 1 for no input, got {}",
        rc
    );
    println!("PASS: no input file case");
}