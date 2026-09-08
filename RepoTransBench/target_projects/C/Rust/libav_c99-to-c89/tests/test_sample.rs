use sample::{add, max, is_even};

#[test]
fn test_add() {
    assert_eq!(add(2, 3), 5);
    assert_eq!(add(-1, 1), 0);
    assert_eq!(add(0, 0), 0);
    assert_eq!(add(-5, -6), -11);
}

#[test]
fn test_max() {
    assert_eq!(max(2, 3), 3);
    assert_eq!(max(5, 1), 5);
    assert_eq!(max(-1, -6), -1);
    assert_eq!(max(7, 7), 7);
}

#[test]
fn test_is_even() {
    assert_eq!(is_even(2), true);
    assert_eq!(is_even(3), false);
    assert_eq!(is_even(0), true);
    assert_eq!(is_even(-4), true);
    assert_eq!(is_even(-5), false);
}