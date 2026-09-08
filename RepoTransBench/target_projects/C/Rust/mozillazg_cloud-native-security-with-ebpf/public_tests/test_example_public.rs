use example::{add, is_even, division};

#[test]
fn test_add() {
    assert_eq!(11, add(4, 7));
    assert_eq!(100, add(60, 40));
    assert_eq!(-9, add(-4, -5));
    assert_eq!(25, add(50, -25));
}

#[test]
fn test_is_even() {
    assert_eq!(true, is_even(102));
    assert_eq!(false, is_even(11));
    assert_eq!(true, is_even(-8));
    assert_eq!(false, is_even(101));
}

#[test]
fn test_division() {
    assert_eq!(5, division(25, 5));
    assert_eq!(-1, division(0, 0));
    assert_eq!(0, division(8, 20));
    assert_eq!(-3, division(9, -3));
}