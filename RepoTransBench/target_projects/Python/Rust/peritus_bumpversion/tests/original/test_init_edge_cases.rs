use peritus_bumpversion;

#[test]
fn test_module_has_expected_minimal_exports() {
    // Should have DESCRIPTION
    let descr = peritus_bumpversion::DESCRIPTION;
    assert!(!descr.is_empty());
}