use crate::parse::parse_args;

#[test]
fn test_parse_additional_args() {
    let args = vec!["-v", "-k", "AnotherKeyword"];
    let parsed = parse_args(&args);
    assert!(args.contains(&"-v"));
    assert_eq!(parsed.k, Some("AnotherKeyword".to_string()));
}