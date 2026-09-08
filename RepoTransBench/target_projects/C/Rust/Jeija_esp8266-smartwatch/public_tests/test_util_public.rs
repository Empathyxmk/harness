use esp8266_smartwatch::util::*;

#[test]
fn test_util_min_max_clamp_public() {
    assert_eq!(util_min(7, 13), 7);
    assert_eq!(util_min(-10, 10), -10);
    assert_eq!(util_max(8, 3), 8);
    assert_eq!(util_max(-8, -5), -5);
    assert_eq!(util_clamp(3, 2, 6), 3);
    assert_eq!(util_clamp(-7, 0, 5), 0);
    assert_eq!(util_clamp(18, 1, 17), 17);
}