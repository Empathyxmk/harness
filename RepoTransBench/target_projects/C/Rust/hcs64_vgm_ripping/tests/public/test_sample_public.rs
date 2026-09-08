use sample::{add, sub};

#[test]
fn test_add() {
    // Different input/output data from possible existing test
    assert_eq!(add(10, 2), 12);         // Simple case
    assert_eq!(add(-3, 7), 4);          // Negative and positive combination
    assert_eq!(add(0, 0), 0);           // Zeroes
    assert_eq!(add(-8, -5), 0);         // Both negative, should return 0 per logic
    assert_eq!(add(15, -5), 10);        // Positive and negative
}

#[test]
fn test_sub() {
    assert_eq!(sub(10, 7), 3);          // Simple subtraction
    assert_eq!(sub(0, 5), -5);          // Zero minus positive
    assert_eq!(sub(-8, -3), -5);        // Both negative
    assert_eq!(sub(22, 22), 0);         // Same numbers
    assert_eq!(sub(-10, 5), -15);       // Negative minus positive
}