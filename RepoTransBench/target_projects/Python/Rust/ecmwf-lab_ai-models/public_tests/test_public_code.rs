#[test]
fn test_public_code_math_ops() {
    let x = 3;
    let y = 9;
    assert_eq!(x * y, 27);
    assert_eq!((y as f64).sqrt(), 3.0);
}

#[test]
fn test_public_code_string_reverse() {
    let s = "abcdef";
    let reversed: String = s.chars().rev().collect();
    assert_eq!(reversed, "fedcba");
}