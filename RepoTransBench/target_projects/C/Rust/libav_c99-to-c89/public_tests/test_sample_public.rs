use sample::{add, max, is_even};

#[test]
fn test_add_public() {
    assert_eq!(add(10, 5), 15);
    assert_eq!(add(-2, 8), 6);
    assert_eq!(add(7, 0), 7);
    assert_eq!(add(-3, -7), -10);
}

#[test]
fn test_max_public() {
    assert_eq!(max(8, 3), 8);
    assert_eq!(max(-5, -2), -2);
    assert_eq!(max(0, -4), 0);
    assert_eq!(max(12, 12), 12);
}

#[test]
fn test_is_even_public() {
    assert_eq!(is_even(10), true);
    assert_eq!(is_even(13), false);
    assert_eq!(is_even(-12), true);
    assert_eq!(is_even(-9), false);
}