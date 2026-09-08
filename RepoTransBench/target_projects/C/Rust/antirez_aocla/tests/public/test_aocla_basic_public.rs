//! Rust translation of antirez_aocla test_aocla_basic_public.c
//! Public test: run with argv0 and an empty string arg (still insufficient args), expects usage exit

use antirez_aocla::aocla_main;

/// Public: call with alternative program name, no input argument, expect exit code 1
#[test]
fn test_no_input_file_case_public() {
    let argv = ["alternative_progname"];
    let rc = aocla_main(1, &argv);
    assert_eq!(
        rc, 1,
        "[PUBLIC] FAIL: Expected exit code 1 for missing input, got {}",
        rc
    );
    println!("PASS: [PUBLIC] no input file case");
}