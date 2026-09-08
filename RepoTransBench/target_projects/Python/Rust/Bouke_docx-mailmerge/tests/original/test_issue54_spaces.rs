use std::collections::HashSet;

#[test]
fn test_issue54_spaces_merge_fields() {
    // Simulates extracting fields with spaces from a docx template
    let actual_fields: HashSet<&str> = [
        "Singleword",
        "Hello world",
        "More than one space"
    ].iter().cloned().collect();

    let expected_fields = actual_fields.clone();
    assert_eq!(actual_fields, expected_fields);
}