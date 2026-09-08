use pywizlight_rust::utils::clamp;

#[test]
fn test_clamp_public() {
    assert_eq!(clamp(135, 100, 140), 135);
    assert_eq!(clamp(90, 100, 140), 100);
    assert_eq!(clamp(145, 100, 140), 140);
}