use pywizlight_rust::bulblibrary::BULB_TYPES;

#[test]
fn test_bulb_type_public() {
    // Positive test
    assert!(BULB_TYPES.contains_key("ESP32_SOCKET"));
    let s = BULB_TYPES.get("ESP32_SOCKET").unwrap();
    assert_eq!(s.bulb_name, "Wiz ESP32 Power Socket");
    assert_eq!(s.feature_set.color, false);

    // Negative test
    assert!(!BULB_TYPES.contains_key("SOCKET_XYZ"));
}