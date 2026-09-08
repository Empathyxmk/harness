use peritus_bumpversion;

#[test]
fn test_main_module_importable_public() {
    let _mod = peritus_bumpversion::__version__;
    assert!(!_mod.is_empty());
}

#[test]
fn test_version_property_existence_public() {
    assert!(peritus_bumpversion::__version__ != "");
    assert!(peritus_bumpversion::__version__.len() > 0);
}