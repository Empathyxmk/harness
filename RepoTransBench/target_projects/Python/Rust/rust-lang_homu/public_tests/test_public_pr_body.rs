use homu_rust::mainmod;

#[test]
fn test_pr_body_contains_diff_key() {
    let body = "Closes #99\nExtra: refactor code";
    assert!(mainmod::pr_body_contains(body, "refactor"));
}

#[test]
fn test_pr_body_not_contains_diff_key() {
    let body = "Implements feature X.\nNone found.";
    assert!(!mainmod::pr_body_contains(body, "security"));
}