// Public test translation from test_main_public.c

use alco_psdump::add;

#[test]
fn test_add_public_positive_numbers() {
    assert_eq!(add(10, 25), 35);
}

#[test]
fn test_add_public_negative_numbers() {
    assert_eq!(add(-8, -6), -14);
}

#[test]
fn test_add_public_mixed_numbers() {
    assert_eq!(add(50, -35), 15);
}