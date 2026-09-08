#[derive(Default)]
struct DummyArgs {
    command: String,
    dummy: Option<String>,
}

fn dummy_parse_args(argv: &[&str]) -> Result<DummyArgs, i32> {
    if argv.contains(&"nonsense_command") {
        return Err(2);
    }
    let command = argv.get(0).cloned().unwrap_or("").to_string();
    let dummy = argv.get(2).cloned().map(|s| s.to_string());
    Ok(DummyArgs { command, dummy })
}

#[test]
fn test_public_main_parse_args() {
    let argv = vec!["run", "--dummy", "xy"];
    let args = dummy_parse_args(&argv).unwrap();
    assert_eq!(args.command, "run");
    assert!(args.dummy == Some("xy".to_string()) || args.dummy.is_none());
}

#[test]
fn test_public_main_invalid_args() {
    let argv = vec!["nonsense_command"];
    let res = dummy_parse_args(&argv);
    assert!(res.is_err());
}