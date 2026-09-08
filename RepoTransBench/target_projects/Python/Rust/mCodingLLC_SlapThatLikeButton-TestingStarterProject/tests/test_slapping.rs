fn divide(x: i32, y: i32) -> i32 {
    x / y
}

#[test]
fn test_basic_slapping() {
    assert_eq!(4 * 2, 8);
}

#[test]
#[should_panic]
fn test_divide_by_zero_panics() {
    let a = 1;
    let b = 0;
    let _ = divide(a, b);
}