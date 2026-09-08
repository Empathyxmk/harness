use example_module::{add, max, abs_diff};

#[test]
fn test_add_public() {
    // Test add function with different data
    assert_eq!(add(6, 4), 10);
    assert_eq!(add(-3, -2), -5);
    assert_eq!(add(100, 200), 300);
}

#[test]
fn test_max_public() {
    // Test max function with different data
    assert_eq!(max(0, -1), 0);
    assert_eq!(max(15, 20), 20);
    assert_eq!(max(-10, -20), -10);
    assert_eq!(max(100, 100), 100);
}

#[test]
fn test_abs_diff_public() {
    // Test abs_diff function with different data
    assert_eq!(abs_diff(50, 45), 5);    // 50 - 45 = 5
    assert_eq!(abs_diff(-6, 5), 11);    // 5 - (-6) = 11
    assert_eq!(abs_diff(0, 100), 100);  // 100 - 0 = 100
}