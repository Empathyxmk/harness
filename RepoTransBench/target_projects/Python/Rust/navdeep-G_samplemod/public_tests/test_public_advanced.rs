use samplemod_rs::core::safe_divide;

#[test]
fn test_safe_divide_normal_public() {
    assert_eq!(safe_divide(15, 3), 5);
}

#[test]
fn test_safe_divide_negative_public() {
    assert_eq!(safe_divide(-9, 3), -3);
}

#[test]
fn test_safe_divide_zero_dividend_public() {
    assert_eq!(safe_divide(0, 2), 0);
}

#[test]
#[should_panic(expected = "Attempt to divide by zero")]
fn test_safe_divide_raises_zero_division_public() {
    let _ = safe_divide(2, 0);
}