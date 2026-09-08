use nerscadmin_ipm::add;

#[test]
fn test_add_positive_numbers() {
    assert_eq!(add(1, 2), 3, "Test failed: add(1, 2) != 3");
}

#[test]
fn test_add_negative_and_positive() {
    assert_eq!(add(-2, 5), 3, "Test failed: add(-2, 5) != 3");
}

#[test]
fn test_add_zeros() {
    assert_eq!(add(0, 0), 0, "Test failed: add(0, 0) != 0");
}