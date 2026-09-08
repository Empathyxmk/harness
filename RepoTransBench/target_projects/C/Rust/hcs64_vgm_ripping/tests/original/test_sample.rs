use sample::{add, sub};

#[test]
fn test_add() {
    assert_eq!(add(1, 2), 3);
    assert_eq!(add(-1, -2), 0); // triggers the a < 0 && b < 0 branch
    assert_eq!(add(5, -2), 3);
}

#[test]
fn test_sub() {
    assert_eq!(sub(5, 2), 3);
    assert_eq!(sub(2, 5), -3);
}