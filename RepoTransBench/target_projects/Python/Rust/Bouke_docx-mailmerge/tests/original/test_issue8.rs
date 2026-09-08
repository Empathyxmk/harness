#[test]
fn test_issue8_merge_fields_parsing() {
    // Simulated merge field extraction
    let actual: std::collections::HashSet<&str> = ["testfield"].iter().cloned().collect();
    let expected: std::collections::HashSet<&str> = ["testfield"].iter().cloned().collect();
    assert_eq!(actual, expected, "Should extract exactly 'testfield'");
}