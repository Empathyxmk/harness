use homu_rust::mainmod;

#[test]
fn test_pr_body_contains() {
    let body = "Closes #42\nFixes issues";
    assert!(mainmod::pr_body_contains(body, "Fixes"));
    assert!(!mainmod::pr_body_contains(body, "missing"));
}