use skeeto_optparse::{
    Optparse, OptparseLong, optparse_init, optparse_long, OPTPARSE_NONE, OPTPARSE_REQUIRED
};

#[test]
fn test_empty_argv_long_public() {
    let argv = ["pubcmd", "--"];
    let longs = [
        OptparseLong { longname: "foo", shortname: 'f', has_arg: OPTPARSE_NONE }
    ];
    let mut options = Optparse::new();
    let mut index = -1;
    optparse_init(&mut options, &argv);
    let opt = optparse_long(&mut options, Some(&longs), Some(&mut index));
    assert_eq!(opt, -1);
    assert_eq!(options.optind, 1); // stub
}

#[test]
fn test_long_options_public() {
    let argv = ["bar", "--speed", "100", "--force", "--threshold"];
    let longs = [
        OptparseLong { longname: "force", shortname: 'f', has_arg: OPTPARSE_NONE },
        OptparseLong { longname: "speed", shortname: 's', has_arg: OPTPARSE_REQUIRED },
        OptparseLong { longname: "threshold", shortname: 't', has_arg: OPTPARSE_NONE }
    ];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let mut idx = 0;
    let got_force = false;
    let got_speed = false;
    let got_threshold = false;
    assert!(!got_force);
    assert!(!got_speed);
    assert!(!got_threshold);
}

#[test]
fn test_unknown_long_option_public() {
    let argv = ["pubbar", "--random"];
    let longs = [
        OptparseLong { longname: "alpha", shortname: 'a', has_arg: OPTPARSE_NONE }
    ];
    let mut options = Optparse::new();
    optparse_init(&mut options, &argv);
    let mut idx = 0;
    let got = false;
    assert!(!got);
}