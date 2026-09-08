use cofyc_argparse_rs::fake_argparse::*;
use std::cell::RefCell;

// Dummy callback for coverage
fn dummy_callback(_self_: &mut Argparse, option: &ArgparseOption) -> i32 {
    let lname = option.long_name.unwrap_or("(null)");
    println!("callback called for {}", lname);
    1234
}

#[test]
fn test_boolean() {
    let mut value: i32 = 0;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Boolean,
            short_name: Some('b'),
            long_name: Some("bool"),
            setter: SetterEnum::Bool(&mut value),
            help: "test boolean",
            callback: Some(dummy_callback),
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    let argv = ["unit", "-b"];
    ap.parse(&argv);
    assert_eq!(value, 1);
}

#[test]
fn test_bit() {
    let mut bits: i32 = 0;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Bit,
            short_name: None,
            long_name: Some("flag"),
            setter: SetterEnum::Int(&mut bits),
            help: "set bit",
            callback: Some(dummy_callback),
            value_bit: 2,
            flags: OptionFlags::empty(),
        },
        ArgparseOption {
            opt_type: OptionType::Bit,
            short_name: None,
            long_name: Some("noflag"),
            setter: SetterEnum::Int(&mut bits),
            help: "clear bit",
            callback: Some(dummy_callback),
            value_bit: 2,
            flags: OptionFlags::NONEG,
        }
    ];
    let mut ap = Argparse::new(options.clone());
    let argv = ["prog", "--flag"];
    ap.parse(&argv);
    assert_eq!(bits, 2);

    // Now clear with --noflag (OPT_NONEG disables negation)
    let argv2 = ["prog", "--noflag"];
    bits = 2;
    let mut ap2 = Argparse::new(options.clone());
    ap2.parse(&argv2);
    assert_eq!(bits, 2); // Still set: OPT_NONEG disables negation
}

#[test]
fn test_string() {
    let mut str_val: Option<String> = None;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::String,
            short_name: Some('s'),
            long_name: Some("str"),
            setter: SetterEnum::String(&mut str_val),
            help: "a string",
            callback: Some(dummy_callback),
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    let argv = ["prog", "-s", "abc"];
    ap.parse(&argv);
    assert!(matches!(str_val, Some(ref s) if s == "abc"));
}

#[test]
fn test_integer() {
    let mut num: i32 = 0;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Integer,
            short_name: Some('n'),
            long_name: Some("num"),
            setter: SetterEnum::Int(&mut num),
            help: "int",
            callback: Some(dummy_callback),
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    let argv = ["prog", "-n", "13"];
    ap.parse(&argv);
    assert_eq!(num, 13);
}

#[test]
fn test_float() {
    let mut val: f32 = 0.0;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Float,
            short_name: Some('f'),
            long_name: Some("flt"),
            setter: SetterEnum::Float(&mut val),
            help: "float",
            callback: Some(dummy_callback),
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    let argv = ["prog", "-f", "2.5"];
    ap.parse(&argv);
    assert!(val > 2.4 && val < 2.6);
}

#[test]
#[should_panic(expected = "missing integer argument")]
fn test_errors() {
    // Test missing integer
    let mut num = 13;
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Integer,
            short_name: Some('n'),
            long_name: Some("num"),
            setter: SetterEnum::Int(&mut num),
            help: "int",
            callback: None,
            value_bit: 0,
            flags: OptionFlags::empty(),
        }
    ];
    let mut ap = Argparse::new(options);
    let argv = ["prog", "-n"];
    ap.parse(&argv); // Should panic (exit in C)
}

#[test]
fn test_group_and_help() {
    let mut options = vec![
        ArgparseOption {
            opt_type: OptionType::Group,
            short_name: None,
            long_name: None,
            setter: SetterEnum::None,
            help: "My group options",
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
    ap.describe("description", "epilog");
    // Do not call parse with --help, as it would exit
}