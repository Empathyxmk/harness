use mrexodia_dumpulator::{add, subtract, multiply, divide};

#[test]
fn test_add() {
    assert_eq!(add(10, 20), 30);
    assert_eq!(add(-5, 15), 10);
    assert_eq!(add(-7, -3), -10);
    assert_eq!(add(0, 0), 0);
}

#[test]
fn test_subtract() {
    assert_eq!(subtract(40, 17), 23);
    assert_eq!(subtract(-8, 15), -23);
    assert_eq!(subtract(-20, -8), -12);
    assert_eq!(subtract(0, 6), -6);
}

#[test]
fn test_multiply() {
    assert_eq!(multiply(3, 7), 21);
    assert_eq!(multiply(-6, 3), -18);
    assert_eq!(multiply(-4, -4), 16);
    assert_eq!(multiply(0, 5), 0);
}

#[test]
fn test_divide() {
    assert_eq!(divide(100, 4), 25);
    assert_eq!(divide(-36, 6), -6);
    assert_eq!(divide(-20, -5), 4);
    assert_eq!(divide(15, 0), 0); // Division by zero returns 0 per implementation
}