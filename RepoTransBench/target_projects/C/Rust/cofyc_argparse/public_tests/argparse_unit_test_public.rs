use cofyc_argparse_rs::fake_argparse::*;

// Dummy callback for coverage
fn dummy_callback(_self_: &mut Argparse, option: &ArgparseOption) -> i32 {
    let lname = option.long_name.unwrap_or("(null)");
    println!("callback called for {}", lname);
    5678
}

#[test]
fn test_boolean_public() {
    let mut value: i32 = 0;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Boolean,
            short_name: Some('c'),
            long_name: Some("check"),
            setter: SetterEnum::Bool(&mut value),
            help: "test boolean public",
            callback: Some(dummy_callback),
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    let argv = ["unit_public", "--check"];
    ap.parse(&argv);
    assert_eq!(value, 1);
}

#[test]
fn test_bit_public() {
    let mut flags: i32 = 0;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Bit,
            short_name: None,
            long_name: Some("debug"),
            setter: SetterEnum::Int(&mut flags),
            help: "set debug",
            callback: Some(dummy_callback),
            value_bit: 4,
            flags: OptionFlags::empty(),
        },
        ArgparseOption {
            opt_type: OptionType::Bit,
            short_name: None,
            long_name: Some("nodebug"),
            setter: SetterEnum::Int(&mut flags),
            help: "clear debug",
            callback: Some(dummy_callback),
            value_bit: 4,
            flags: OptionFlags::NONEG,
        }
    ];
    let mut ap = Argparse::new(options.clone());
    let argv = ["prog_public", "--debug"];
    ap.parse(&argv);
    assert_eq!(flags, 4);

    let argv2 = ["prog_public", "--nodebug"];
    flags = 4;
    let mut ap2 = Argparse::new(options.clone());
    ap2.parse(&argv2);
    assert_eq!(flags, 4); // OPT_NONEG disables negation, still set
}

#[test]
fn test_string_public() {
    let mut str_val: Option<String> = None;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::String,
            short_name: Some('t'),
            long_name: Some("text"),
            setter: SetterEnum::String(&mut str_val),
            help: "a string public",
            callback: Some(dummy_callback),
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    let argv = ["prog_public", "-t", "xyz"];
    ap.parse(&argv);
    assert!(matches!(str_val, Some(ref s) if s == "xyz"));
}

#[test]
fn test_integer_public() {
    let mut num: i32 = 0;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Integer,
            short_name: Some('m'),
            long_name: Some("mode"),
            setter: SetterEnum::Int(&mut num),
            help: "int public",
            callback: Some(dummy_callback),
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    let argv = ["prog_public", "-m", "27"];
    ap.parse(&argv);
    assert_eq!(num, 27);
}

#[test]
fn test_float_public() {
    let mut val: f32 = 0.0;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Float,
            short_name: Some('z'),
            long_name: Some("zoom"),
            setter: SetterEnum::Float(&mut val),
            help: "float public",
            callback: Some(dummy_callback),
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    let argv = ["prog_public", "-z", "6.75"];
    ap.parse(&argv);
    assert!(val > 6.7 && val < 6.8);
}

#[test]
fn test_group_and_help_public() {
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Group,
            short_name: None,
            long_name: None,
            setter: SetterEnum::None,
            help: "Public group options",
            callback: None,
            value_bit: 0,
            flags: OptionFlags::empty(),
        },
        ArgparseOption {
            opt_type: OptionType::Help,
            short_name: None,
            long_name: None,
            setter: SetterEnum::None,
            help: "help",
            callback: None,
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    ap.describe("public description", "public epilog");
    // Don't call parse with --help, as it will panic (would exit in C).
}