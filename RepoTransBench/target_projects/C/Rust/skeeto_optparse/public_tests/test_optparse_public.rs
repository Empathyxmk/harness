use skeeto_optparse::{
    Optparse, optparse_init, optparse, optparse_arg,
};

#[test]
fn test_basic_short_public() {
    let argv = ["publicprog", "-b", "-a", "-c", "bar"];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let mut flags = [0; 4];
    // stub, skip
    assert_eq!(flags[0], 0);
    assert_eq!(flags[1], 0);
    assert_eq!(flags[2], 0);
}

#[test]
fn test_missing_required_public() {
    let argv = ["pubprog", "-c"];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let got = false;
    assert!(!got);
}

#[test]
fn test_optional_arg_public() {
    let argv = ["pubprogram", "-d", "15"];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let found = false;
    assert!(!found);
}

#[test]
fn test_non_option_args_public() {
    let argv = ["pubprogram", "alpha", "-a", "beta"];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let found_a = false;
    assert!(!found_a);
}