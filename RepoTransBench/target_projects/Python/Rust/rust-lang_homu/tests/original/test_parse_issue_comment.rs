use homu_rust::parse_issue_comment;

#[test]
fn test_parse_command_cases() {
    assert_eq!(
        parse_issue_comment::parse_command("@homu: retry"),
        ("retry".to_string(), "".to_string())
    );
    assert_eq!(
        parse_issue_comment::parse_command("@homu: clean foo"),
        ("clean".to_string(), "foo".to_string())
    );
}