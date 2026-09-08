use esp8266_smartwatch::util::*;

#[test]
fn test_util_min_max_clamp() {
    assert_eq!(util_min(2, 3), 2);
    assert_eq!(util_min(10, -3), -3);
    assert_eq!(util_max(2, 3), 3);
    assert_eq!(util_max(10, -3), 10);
    assert_eq!(util_clamp(1, 0, 2), 1);
    assert_eq!(util_clamp(-1, 0, 2), 0);
    assert_eq!(util_clamp(5, 0, 2), 2);
}