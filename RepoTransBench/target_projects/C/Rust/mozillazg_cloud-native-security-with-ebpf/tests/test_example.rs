use example::{add, is_even, division};

#[test]
fn test_add() {
    assert_eq!(3, add(1, 2));
    assert_eq!(-1, add(-3, 2));
    assert_eq!(0, add(0, 0));
    assert_eq!(20, add(10, 10));
}

#[test]
fn test_is_even() {
    assert_eq!(true, is_even(4));
    assert_eq!(false, is_even(7));
    assert_eq!(true, is_even(0));
    assert_eq!(false, is_even(-3));
}

#[test]
fn test_division() {
    assert_eq!(2, division(6, 3));
    assert_eq!(-1, division(1, 0)); // divided by zero
    assert_eq!(0, division(0, 5));
    assert_eq!(-2, division(-10, 5));
}