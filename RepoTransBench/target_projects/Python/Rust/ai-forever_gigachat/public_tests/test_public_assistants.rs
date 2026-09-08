#[test]
fn test_public_assistant_list_behavior() {
    let assistants = vec![
        ("asst_753", "HelperA", "Helps with numbers."),
        ("asst_111", "HelperB", "Helps with words."),
    ];
    assert_eq!(assistants[0].1, "HelperA");
    assert!(assistants[1].2.starts_with("Helps with"));
}

#[test]
fn test_public_assistant_detail_fields() {
    let assistant = ("asst_xyz", "XBot", "Handles X-cases");
    assert_eq!(assistant.0, "asst_xyz");
    assert_eq!(assistant.1, "XBot");
    assert_eq!(assistant.2, "Handles X-cases");
}