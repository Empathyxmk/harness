use mrexodia_dumpulator::{add, subtract, multiply, divide};

#[test]
fn test_add() {
    assert_eq!(add(2, 3), 5);
    assert_eq!(add(-1, 1), 0);
    assert_eq!(add(0, 0), 0);
}

#[test]
fn test_subtract() {
    assert_eq!(subtract(5, 3), 2);
    assert_eq!(subtract(0, 5), -5);
    assert_eq!(subtract(7, 7), 0);
}

#[test]
fn test_multiply() {
    assert_eq!(multiply(3, 4), 12);
    assert_eq!(multiply(-2, 3), -6);
    assert_eq!(multiply(0, 10), 0);
}

#[test]
fn test_divide() {
    assert_eq!(divide(10, 2), 5);
    assert_eq!(divide(10, 3), 3);
    assert_eq!(divide(10, 0), 0); // division by zero case
}