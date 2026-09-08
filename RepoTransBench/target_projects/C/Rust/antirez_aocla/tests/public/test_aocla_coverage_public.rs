//! Rust translation of antirez_aocla test_aocla_coverage_public.c
//! Public test: run with different dummy input file name, should "run" successfully

use antirez_aocla::aocla_main;

/// Public: call with alternative program name, dummy .aocla file, expect exit code 0
#[test]
fn test_dummy_input_file_case_public() {
    let argv = ["alternative_progname", "public_test_script.aocla"];
    let rc = aocla_main(2, &argv);
    assert_eq!(
        rc, 0,
        "[PUBLIC] FAIL: Expected exit code 0 for input file present, got {}",
        rc
    );
    println!("PASS: [PUBLIC] dummy input file case");
}