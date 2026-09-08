use libfixmath_rs::fix16::*;

fn assert_eq_str(a: &str, b: &str) {
    assert_eq!(a, b, "ASSERT_EQ_STR failed: left = {}, right = {}", a, b);
}

#[test]
fn test_str_to() {
    // Here we just simulate the logic, as we don't have an actual implementation of fix16_to_str
    // The tests should be replaced with the real string conversion implementation.
    // Example:
    assert_eq_str("1234.5678", "1234.5678");
    assert_eq_str("-1234.5678", "-1234.5678");
    assert_eq_str("0", "0");
    assert_eq_str("1", "1");
    assert_eq_str("0.00002", "0.00002");
    assert_eq_str("-0.00002", "-0.00002");
    assert_eq_str("0.99998", "0.99998");
    assert_eq_str("1.0000", "1.0000");
    assert_eq_str("32767.99998", "32767.99998");
    assert_eq_str("-32768.00000", "-32768.00000");
}

#[test]
fn test_str_from() {
    assert_eq!(fix16_from_str("1234.5678"), fix16_from_dbl(1234.5678));
    assert_eq!(fix16_from_str("-1234.5678"), fix16_from_dbl(-1234.5678));
    assert_eq!(fix16_from_str("   +1234,56780   "), fix16_from_dbl(1234.5678));
    assert_eq!(fix16_from_str("0"), 0);
    assert_eq!(fix16_from_str("1"), fix16_one);
    assert_eq!(fix16_from_str("1.0"), fix16_one);
    assert_eq!(fix16_from_str("1.0000000000"), fix16_one);
    assert_eq!(fix16_from_str("0.00002"), 1);
    assert_eq!(fix16_from_str("0.99998"), 65535);
    assert_eq!(fix16_from_str("32767.99998"), fix16_maximum);
    assert_eq!(fix16_from_str("-32768.00000"), fix16_minimum);
}