use crate::parse::parse_args;

#[test]
fn test_parse_args_fake_strict() {
    let args = vec!["--strict", "--color", "always"];
    let parsed = parse_args(&args);
    assert!(parsed.strict);
    assert_eq!(parsed.color, Some("always".to_string()));
}