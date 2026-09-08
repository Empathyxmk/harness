use peritus_bumpversion as bumpversion;

#[test]
fn test_public_api_includes_description() {
    assert!(!bumpversion::DESCRIPTION.is_empty());
}

#[test]
fn test_main_module_importable() {
    // In Rust, module import is by "extern crate" or use. This test is trivial.
    let _x = bumpversion::DESCRIPTION;
}