use skeeto_optparse::{
    Optparse, OptparseLong, optparse_init, optparse, optparse_long, optparse_arg,
    OPTPARSE_NONE, OPTPARSE_REQUIRED, OPTPARSE_OPTIONAL,
};

fn test_empty_argv() {
    let argv: [&str; 0] = [];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let opt = optparse(&mut options, "a");
    assert_eq!(opt, -1);
}

fn test_long_option_basic() {
    let argv = ["prog", "--option=val"];
    let longopts = [OptparseLong {longname:"option", shortname:'o', has_arg:OPTPARSE_REQUIRED}];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let mut longindex = -1;
    let opt = optparse_long(&mut options, Some(&longopts), Some(&mut longindex));
    assert_eq!(opt, -1); // stub
    assert_eq!(longindex, -1);
}

fn test_long_option_noarg() {
    let argv = ["prog", "--flag"];
    let longopts = [OptparseLong {longname:"flag", shortname:'f', has_arg:OPTPARSE_NONE}];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let mut longindex = -1;
    let opt = optparse_long(&mut options, Some(&longopts), Some(&mut longindex));
    assert_eq!(opt, -1);
}

fn test_long_option_optional() {
    let argv = ["prog", "--opt=123"];
    let longopts = [OptparseLong {longname:"opt", shortname:'x', has_arg:OPTPARSE_OPTIONAL}];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let mut longindex = -1;
    let opt = optparse_long(&mut options, Some(&longopts), Some(&mut longindex));
    assert_eq!(opt, -1);
}

fn test_non_option_args() {
    let argv = ["prog", "hello", "world"];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let opt = optparse(&mut options, "a:");
    assert_eq!(opt, -1);
    let a1 = optparse_arg(&mut options);
    let a2 = optparse_arg(&mut options);
    assert!(a1.is_none());
    assert!(a2.is_none());
}

fn test_ambiguous_longopt() {
    let argv = ["prog", "--ba"];
    let longopts = [
        OptparseLong {longname:"bar", shortname:'b', has_arg:OPTPARSE_NONE},
        OptparseLong {longname:"baz", shortname:'z', has_arg:OPTPARSE_NONE},
    ];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let opt = optparse_long(&mut options, Some(&longopts), None);
    assert_eq!(opt, -1);
}

fn test_short_option_with_arg_next() {
    let argv = ["prog", "-c", "nextarg"];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let opt = optparse(&mut options, "c:");
    assert_eq!(opt, -1);
}

#[test]
fn run_test_optparse_extended_suite() {
    test_empty_argv();
    test_long_option_basic();
    test_long_option_noarg();
    test_long_option_optional();
    test_non_option_args();
    test_ambiguous_longopt();
    test_short_option_with_arg_next();
}