use homu_rust::parse_issue_comment;

#[test]
fn test_parse_command_custom_case() {
    assert_eq!(
        parse_issue_comment::parse_command("@homu: test-queue"),
        ("test-queue".to_string(), "".to_string())
    );
}

#[test]
fn test_parse_command_argumented() {
    assert_eq!(
        parse_issue_comment::parse_command("@homu: clean bar"),
        ("clean".to_string(), "bar".to_string())
    );
}