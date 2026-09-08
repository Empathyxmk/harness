struct Args {
    file: String,
    verbose: bool,
}

fn get_args(args: &[&str]) -> Args {
    // simple simulation
    if args.is_empty() {
        panic!("SystemExit");
    }
    let file = args
        .iter()
        .find(|s| s.ends_with(".png"))
        .map(|s| s.to_string())
        .unwrap_or("".to_string());
    let verbose = args.iter().any(|&s| s == "-v" || s == "--");
    Args { file, verbose }
}

#[test]
fn test_get_args_qrcode() {
    let args = get_args(&["barcode_testimage.png"]);
    assert_eq!(args.file, "barcode_testimage.png");
    let args2 = get_args(&["-v", "--", "other"]);
    assert!(args2.verbose);
}

#[test]
#[should_panic(expected = "SystemExit")]
fn test_main_no_file() {
    let _ = get_args(&[]);
}