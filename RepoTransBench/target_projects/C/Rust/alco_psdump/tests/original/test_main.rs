// Original test translation from test_main.c

use alco_psdump::add;

#[test]
fn test_add_positive_numbers() {
    assert_eq!(add(1, 2), 3);
}

#[test]
fn test_add_negative_numbers() {
    assert_eq!(add(-4, -5), -9);
}

#[test]
fn test_add_mixed_numbers() {
    assert_eq!(add(7, -2), 5);
}