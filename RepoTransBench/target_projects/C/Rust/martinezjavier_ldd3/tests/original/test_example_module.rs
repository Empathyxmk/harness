use example_module::{add, max, abs_diff};

#[test]
fn test_add() {
    // Test add function
    assert_eq!(add(1, 2), 3);
    assert_eq!(add(-5, 5), 0);
    assert_eq!(add(0, 0), 0);
}

#[test]
fn test_max() {
    // Test max function
    assert_eq!(max(1, 2), 2);
    assert_eq!(max(7, 3), 7);
    assert_eq!(max(-2, -5), -2);
    assert_eq!(max(0, 0), 0);
}

#[test]
fn test_abs_diff() {
    // Test abs_diff function
    assert_eq!(abs_diff(10, 4), 6);   // 10 - 4 = 6
    assert_eq!(abs_diff(3, 8), 5);    // 8 - 3 = 5
    assert_eq!(abs_diff(7, 7), 0);    // 7 - 7 = 0
}