fn divide(x: i32, y: i32) -> i32 {
    x / y
}

#[test]
fn test_public_slapping_works() {
    assert_eq!(5 + 5, 10);
}

#[test]
#[should_panic]
fn test_public_divide_by_zero_panics() {
    let a = 42;
    let b = 0;
    let _ = divide(a, b);
}