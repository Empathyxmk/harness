use nerscadmin_ipm::{add, multiply};

#[test]
fn test_add_different_positive_numbers() {
    assert_eq!(add(2, 4), 6, "Public Test failed: add(2, 4) != 6");
}

#[test]
fn test_add_negative_and_positive_different() {
    assert_eq!(add(-5, 8), 3, "Public Test failed: add(-5, 8) != 3");
}

#[test]
fn test_add_equal_opposite_numbers() {
    assert_eq!(add(10, -10), 0, "Public Test failed: add(10, -10) != 0");
}

// From the gcov file, we can see there were also multiply tests
#[test]
fn test_multiply_positive_numbers() {
    assert_eq!(multiply(4, 5), 20);
}

#[test]
fn test_multiply_negative_and_positive() {
    assert_eq!(multiply(-2, 7), -14);
}