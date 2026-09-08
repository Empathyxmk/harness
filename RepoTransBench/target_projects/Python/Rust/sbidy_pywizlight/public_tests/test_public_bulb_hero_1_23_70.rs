use pywizlight_rust::bulblibrary::BULB_TYPES;

#[test]
fn test_bulb_hero_1_23_70_public() {
    // Use a different HERO model name (fictional for public case)
    assert!(!BULB_TYPES.contains_key("HERO_PUBLIC"));
    // Check the existing bulb is still correct for interface, just different data
    let b = BULB_TYPES.get("ESP01_SHDW_12WW").unwrap();
    assert_eq!(b.feature_set.color, false);
}